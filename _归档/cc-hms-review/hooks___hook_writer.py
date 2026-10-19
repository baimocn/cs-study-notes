"""
HookWriter — 多进程安全的 vmem 写入器

所有 Hook 脚本通过此类写入数据库，使用跨平台文件锁协调多进程并发写入。
- Linux/macOS: fcntl.flock
- Windows: msvcrt.locking

使用方式：
    from _hook_writer import HookWriter
    with HookWriter(db_path) as writer:
        writer.store(...)
        writer.profile_set(...)
"""

import os
import sys
import time
from pathlib import Path

# 确保 vmem 可导入
_HOOKS_DIR = Path(__file__).parent
_MCP_DIR = Path.home() / ".claude" / "mcp-servers"
if str(_MCP_DIR) not in sys.path:
    sys.path.insert(0, str(_MCP_DIR))
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

# 跨平台文件锁
try:
    import fcntl
    _LOCK_TYPE = "fcntl"
except ImportError:
    try:
        import msvcrt
        _LOCK_TYPE = "msvcrt"
    except ImportError:
        _LOCK_TYPE = "none"


class HookWriter:
    """
    多进程安全的 vmem 写入器。

    使用文件锁（flock on Unix, LockFileEx on Windows）确保同一时刻
    只有一个进程在写入数据库，避免 "database is locked" 错误。

    锁文件位于数据库同目录下，命名为 <db_name>.lock。

    Args:
        db_path: SQLite 数据库文件路径。
        timeout_sec: 获取锁的超时时间（秒），默认 3 秒。
                     超时后自动放弃并返回 False，不抛出异常。
    """

    def __init__(self, db_path: str, timeout_sec: float = 3.0):
        self._db_path = db_path
        self._timeout = timeout_sec
        self._lock_path = str(db_path) + ".lock"
        self._lock_fd = None
        self._store = None
        self._locked = False

    # ------------------------------------------------------------------
    # 上下文管理器
    # ------------------------------------------------------------------

    def __enter__(self):
        self._acquire_lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.close()
        except Exception:
            pass
        return False  # 不抑制异常

    # ------------------------------------------------------------------
    # 锁管理
    # ------------------------------------------------------------------

    def _acquire_lock(self) -> bool:
        """
        尝试获取文件锁。超时返回 False。
        """
        if self._locked:
            return True

        # 确保锁文件目录存在
        lock_dir = os.path.dirname(self._lock_path)
        if lock_dir:
            os.makedirs(lock_dir, exist_ok=True)

        try:
            self._lock_fd = os.open(
                self._lock_path,
                os.O_CREAT | os.O_RDWR,
            )
        except Exception as e:
            print(f"[hook_writer] cannot open lock file: {e}", file=sys.stderr)
            return False

        deadline = time.monotonic() + self._timeout
        wait_interval = 0.01  # 10ms 轮询间隔

        while True:
            try:
                if self._try_lock():
                    self._locked = True
                    return True
            except Exception:
                pass

            if time.monotonic() >= deadline:
                print(
                    f"[hook_writer] lock timeout ({self._timeout}s) for {self._db_path}",
                    file=sys.stderr,
                )
                self._close_lock_fd()
                return False

            time.sleep(wait_interval)
            wait_interval = min(wait_interval * 1.5, 0.2)  # 渐进式等待，最长 200ms

    def _try_lock(self) -> bool:
        """非阻塞尝试加锁。成功返回 True。"""
        if _LOCK_TYPE == "fcntl":
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except (BlockingIOError, OSError):
                return False

        elif _LOCK_TYPE == "msvcrt":
            try:
                # 锁定整个文件
                os.lseek(self._lock_fd, 0, os.SEEK_SET)
                msvcrt.locking(self._lock_fd, msvcrt.LK_NBLCK, 1)
                return True
            except (OSError, OverflowError):
                return False

        else:
            # 没有可用的锁机制，直接返回 True（降级为无锁）
            return True

    def _release_lock(self) -> None:
        """释放文件锁。"""
        if not self._locked or self._lock_fd is None:
            return

        try:
            if _LOCK_TYPE == "fcntl":
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            elif _LOCK_TYPE == "msvcrt":
                try:
                    os.lseek(self._lock_fd, 0, os.SEEK_SET)
                    msvcrt.locking(self._lock_fd, msvcrt.LK_UNLCK, 1)
                except Exception:
                    pass
        except Exception:
            pass

        self._close_lock_fd()
        self._locked = False

    def _close_lock_fd(self) -> None:
        if self._lock_fd is not None:
            try:
                os.close(self._lock_fd)
            except Exception:
                pass
            self._lock_fd = None

    # ------------------------------------------------------------------
    # Store 访问（懒加载）
    # ------------------------------------------------------------------

    def _get_store(self):
        """懒加载 MemoryVectorStore。"""
        if self._store is None:
            from vmem.store import MemoryVectorStore
            self._store = MemoryVectorStore(db_path=self._db_path)
        return self._store

    @property
    def store(self):
        """获取底层 MemoryVectorStore 实例（已持锁）。"""
        return self._get_store()

    # ------------------------------------------------------------------
    # 便捷写入方法（均返回 bool，失败不抛异常）
    # ------------------------------------------------------------------

    def store_memory(self, key: str, value: str, source: str = "",
                     level: str = "", tags: str = "",
                     related=None, embedding=None) -> bool:
        """写入一条记忆。成功返回 True。"""
        if not self._locked:
            return False
        try:
            return self._get_store().store(
                key=key, value=value, source=source, level=level,
                tags=tags, related=related, embedding=embedding,
            )
        except Exception as e:
            print(f"[hook_writer] store_memory error: {e}", file=sys.stderr)
            return False

    def causal_add(self, from_key: str, to_key: str,
                   relation: str, strength: float = 1.0) -> bool:
        """添加因果链。成功返回 True。"""
        if not self._locked:
            return False
        try:
            return self._get_store().causal_add(
                from_key, to_key, relation, strength,
            )
        except Exception as e:
            print(f"[hook_writer] causal_add error: {e}", file=sys.stderr)
            return False

    def link_add(self, from_key: str, to_key: str,
                 link_type: str, strength: float = 1.0) -> bool:
        """添加记忆关联。成功返回 True。"""
        if not self._locked:
            return False
        try:
            return self._get_store().link_add(
                from_key, to_key, link_type, strength,
            )
        except Exception as e:
            print(f"[hook_writer] link_add error: {e}", file=sys.stderr)
            return False

    def profile_set(self, attr_key: str, attr_value: str,
                    category: str, confidence: float = 0.5,
                    source: str = "auto") -> bool:
        """设置 profile 属性。成功返回 True。"""
        if not self._locked:
            return False
        try:
            return self._get_store().profile_set(
                attr_key, attr_value, category, confidence, source,
            )
        except Exception as e:
            print(f"[hook_writer] profile_set error: {e}", file=sys.stderr)
            return False

    def profile_get(self, attr_key: str = None, category: str = None) -> list:
        """读取 profile 属性。失败返回空列表。"""
        if not self._locked:
            return []
        try:
            return self._get_store().profile_get(attr_key, category)
        except Exception as e:
            print(f"[hook_writer] profile_get error: {e}", file=sys.stderr)
            return []

    def search_fts(self, query: str, top_k: int = 10) -> list:
        """FTS 搜索。失败返回空列表。"""
        if not self._locked:
            return []
        try:
            return self._get_store().search_fts(query, top_k)
        except Exception as e:
            print(f"[hook_writer] search_fts error: {e}", file=sys.stderr)
            return []

    def get(self, key: str) -> dict:
        """获取单条记忆。失败返回 None。"""
        if not self._locked:
            return None
        try:
            return self._get_store().get(key)
        except Exception as e:
            print(f"[hook_writer] get error: {e}", file=sys.stderr)
            return None

    def list_all(self, limit: int = 100, source_filter: str = None) -> list:
        """列出记忆。失败返回空列表。"""
        if not self._locked:
            return []
        try:
            return self._get_store().list_all(limit, source_filter)
        except Exception as e:
            print(f"[hook_writer] list_all error: {e}", file=sys.stderr)
            return []

    def introspect_gc(self, max_age_days: int = 30,
                      min_confidence: float = 0.2) -> list:
        """执行 GC。失败返回空列表。"""
        if not self._locked:
            return []
        try:
            return self._get_store().introspect_gc(max_age_days, min_confidence)
        except Exception as e:
            print(f"[hook_writer] introspect_gc error: {e}", file=sys.stderr)
            return []

    def introspect_health(self) -> dict:
        """获取健康报告。失败返回空 dict。"""
        if not self._locked:
            return {}
        try:
            return self._get_store().introspect_health()
        except Exception as e:
            print(f"[hook_writer] introspect_health error: {e}", file=sys.stderr)
            return {}

    def find_duplicates(self, threshold: float = 0.92, chunk_size: int = 1000) -> list:
        """查找重复记忆对。失败返回空列表。"""
        if not self._locked:
            return []
        try:
            return self._get_store().find_duplicates(
                threshold=threshold, chunk_size=chunk_size,
            )
        except Exception as e:
            print(f"[hook_writer] find_duplicates error: {e}", file=sys.stderr)
            return []

    def merge_memories(self, key_a: str, key_b: str, strategy: str = "keep_richer") -> dict:
        """合并两条记忆。失败返回空 dict。"""
        if not self._locked:
            return {}
        try:
            return self._get_store().merge_memories(key_a, key_b, strategy=strategy)
        except Exception as e:
            print(f"[hook_writer] merge_memories error: {e}", file=sys.stderr)
            return {}

    # ------------------------------------------------------------------
    # 直接 SQLite 写入（用于需要绕过 MemoryVectorStore 的场景）
    # ------------------------------------------------------------------

    def raw_conn(self):
        """获取原生 sqlite3 连接。调用方需自行管理事务。"""
        if not self._locked:
            return None
        try:
            return self._get_store()._get_conn()
        except Exception as e:
            print(f"[hook_writer] raw_conn error: {e}", file=sys.stderr)
            return None

    # ------------------------------------------------------------------
    # 清理
    # ------------------------------------------------------------------

    def close(self) -> None:
        """关闭 store 并释放锁。"""
        try:
            if self._store is not None:
                self._store.close()
                self._store = None
        finally:
            self._release_lock()
