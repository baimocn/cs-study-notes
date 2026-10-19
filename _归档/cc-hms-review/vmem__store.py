"""
向量记忆存储层 — MemoryVectorStore
SQLite + FTS5 + numpy 余弦相似度 + sentence-transformers embedding
"""

import base64
import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

# ---------------------------------------------------------------------------
# EmbeddingEngine — 懒加载 bge-small-zh-v1.5
# ---------------------------------------------------------------------------

class EmbeddingEngine:
    """基于 sentence-transformers 的嵌入引擎，输出 float32[512] 归一化向量。"""

    def __init__(self, model_path: str = None):
        if model_path is None:
            from vmem.config import MODEL_PATH
            model_path = MODEL_PATH
        self._model_path = model_path
        self._model = None

    def _ensure_loaded(self):
        if self._model is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_path)

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        将文本列表编码为 float32[512] 归一化向量。
        返回 shape = (len(texts), 512) 的 numpy 数组。
        """
        self._ensure_loaded()
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        # 确保 shape 正确
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        return embeddings.astype(np.float32)


# ---------------------------------------------------------------------------
# ConnectionPool — 线程安全的 SQLite 连接池
# ---------------------------------------------------------------------------

class ConnectionPool:
    """
    线程安全的 SQLite 连接池。

    每个线程获得独立的连接（SQLite 连接不是线程安全的）。
    支持连接健康检查，自动重建失效连接。
    使用 threading.Lock 保护池的内部状态。

    Args:
        db_path: SQLite 数据库文件路径。
        max_connections: 最大连接数（默认 3）。实际按线程 ID 管理，
                         此参数限制池的总容量，超出后关闭最久未使用的。
    """

    def __init__(self, db_path: str, max_connections: int = 3):
        self._db_path = db_path
        self._max = max_connections
        self._lock = threading.Lock()
        # key: thread_id, value: (connection, last_used_timestamp)
        self._pool: Dict[int, tuple] = {}

    def _create_connection(self) -> sqlite3.Connection:
        """创建一个新的 SQLite 连接并配置 PRAGMA。"""
        conn = sqlite3.connect(self._db_path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def _is_connection_alive(self, conn: sqlite3.Connection) -> bool:
        """检查连接是否仍然有效。"""
        try:
            conn.execute("SELECT 1").fetchone()
            return True
        except Exception:
            return False

    def get(self) -> sqlite3.Connection:
        """
        获取当前线程的连接。

        如果当前线程已有有效连接则复用；否则创建新连接。
        如果池已满，关闭最久未使用的连接以腾出空间。
        """
        tid = threading.get_ident()
        with self._lock:
            entry = self._pool.get(tid)
            if entry is not None:
                conn, _ = entry
                if self._is_connection_alive(conn):
                    # 更新使用时间
                    self._pool[tid] = (conn, time.time())
                    return conn
                # 连接失效，移除
                try:
                    conn.close()
                except Exception:
                    pass
                del self._pool[tid]

            # 需要新建连接
            if len(self._pool) >= self._max:
                # 驱逐最久未使用的
                oldest_tid = min(self._pool, key=lambda t: self._pool[t][1])
                old_conn, _ = self._pool.pop(oldest_tid)
                try:
                    old_conn.close()
                except Exception:
                    pass

            conn = self._create_connection()
            self._pool[tid] = (conn, time.time())
            return conn

    def close_all(self) -> None:
        """关闭池中所有连接。"""
        with self._lock:
            for conn, _ in self._pool.values():
                try:
                    conn.close()
                except Exception:
                    pass
            self._pool.clear()

    def close_current(self) -> None:
        """关闭当前线程的连接（如果存在）。"""
        tid = threading.get_ident()
        with self._lock:
            entry = self._pool.pop(tid, None)
            if entry is not None:
                try:
                    entry[0].close()
                except Exception:
                    pass

    @property
    def size(self) -> int:
        """当前池中的连接数。"""
        with self._lock:
            return len(self._pool)


# ---------------------------------------------------------------------------
# MemoryVectorStore
# ---------------------------------------------------------------------------

class MemoryVectorStore:
    """
    单 SQLite 文件的向量记忆存储。
    - memory_vectors: 结构化数据 + float32[512] embedding
    - memory_fts:     FTS5 trigram 全文索引 (key, value, source, tags)
    - 融合搜索: 0.60*向量 + 0.25*全文 + 0.15*时间衰减
    """

    DB_PATH = None  # 由 config 模块提供默认值
    EMBED_DIM = 512
    MAX_RETRIES = 3
    RETRY_BACKOFF_MS = [50, 100, 200]  # 指数退避（毫秒）

    def __init__(
        self,
        db_path: Optional[str] = None,
        embedding_engine: Optional[EmbeddingEngine] = None,
        max_connections: int = 3,
    ):
        if db_path is None:
            from vmem.config import DB_PATH
            db_path = DB_PATH
        self._db_path = db_path or self.DB_PATH
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)

        self._engine = embedding_engine or EmbeddingEngine()
        self._pool = ConnectionPool(self._db_path, max_connections=max_connections)
        # 保留 _conn 属性用于向后兼容（初始化为 None，按需从 pool 获取）
        self._conn: Optional[sqlite3.Connection] = None
        self._topic_counter = 0  # tracks new memories since last topic recalc

        self._init_db()

    # ------------------------------------------------------------------
    # 数据库初始化
    # ------------------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        """从连接池获取当前线程的连接。"""
        return self._pool.get()

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memory_vectors (
                key         TEXT PRIMARY KEY,
                value       TEXT NOT NULL,
                source      TEXT DEFAULT '',
                importance  TEXT DEFAULT '',
                tags        TEXT DEFAULT '',
                related     TEXT DEFAULT '[]',
                embedding   BLOB,
                created_at  INTEGER NOT NULL,
                updated_at  INTEGER NOT NULL
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                key, value, source, tags,
                tokenize='trigram'
            );
        """)
        conn.commit()

        # Run schema migrations (D-09, D-10)
        from vmem.migrations import run_migrations
        run_migrations(conn)

    # ------------------------------------------------------------------
    # 公共方法
    # ------------------------------------------------------------------

    def store(
        self,
        key: str,
        value: str,
        source: str = "",
        level: str = "",
        tags: str = "",
        related: Optional[List[str]] = None,
        embedding: Optional[np.ndarray] = None,
    ) -> bool:
        """
        INSERT OR REPLACE 一条记忆。
        如果未提供 embedding，自动用 EmbeddingEngine 编码 value。
        注意：level 参数名保持不变（向后兼容），写入 importance 列。

        所有后续操作（FTS 同步、自动关联、置信度初始化、衰减初始化、话题聚类）
        都在同一个事务中完成，支持最多 3 次重试（指数退避 50ms/100ms/200ms）。
        写入失败时记录错误日志但不抛异常，保证 Hook 不中断主流程。
        """
        # Encoding is done outside the retry loop (it's I/O-bound, not DB-bound)
        try:
            if embedding is None:
                embedding = self._engine.encode([value])[0]
            embedding_blob = embedding.astype(np.float32).tobytes()
        except Exception as e:
            print(f"[vmem] store encoding error: {e}")
            return False

        related_json = json.dumps(related or [], ensure_ascii=False)

        # Convert tags to JSON array (D-07)
        if isinstance(tags, str) and tags:
            tags_json = json.dumps([t.strip() for t in tags.split(",") if t.strip()], ensure_ascii=False)
        elif isinstance(tags, list):
            tags_json = json.dumps(tags, ensure_ascii=False)
        else:
            tags_json = "[]"

        # FTS tags string
        if isinstance(tags, str):
            fts_tags = tags
        elif isinstance(tags, list):
            fts_tags = ",".join(tags)
        else:
            fts_tags = ""

        # Retry loop with exponential backoff
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                self._store_transaction(
                    key=key,
                    value=value,
                    source=source,
                    level=level,
                    tags_json=tags_json,
                    fts_tags=fts_tags,
                    related_json=related_json,
                    embedding_blob=embedding_blob,
                )
                return True
            except sqlite3.OperationalError as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    backoff = self.RETRY_BACKOFF_MS[attempt] / 1000.0
                    time.sleep(backoff)
                    continue
                break
            except Exception as e:
                last_error = e
                break

        print(f"[vmem] store error (after {self.MAX_RETRIES} retries): {last_error}")
        return False

    def _store_transaction(
        self,
        key: str,
        value: str,
        source: str,
        level: str,
        tags_json: str,
        fts_tags: str,
        related_json: str,
        embedding_blob: bytes,
    ) -> None:
        """
        在一个事务内完成 store 的所有数据库操作。

        包括：memory_vectors 插入、FTS 同步、自动关联、置信度初始化、
        衰减初始化、话题聚类。

        使用 BEGIN IMMEDIATE 提前获取写锁，避免死锁。
        调用方负责重试和错误处理。
        """
        conn = self._get_conn()
        now = int(time.time())

        conn.execute("BEGIN IMMEDIATE")
        try:
            # 查旧记录的 created_at 和 confidence（Phase 5: 保留已有置信度）
            row = conn.execute(
                "SELECT created_at, confidence FROM memory_vectors WHERE key = ?",
                (key,),
            ).fetchone()
            created_at = row[0] if row else now
            existing_confidence = row[1] if row else None

            conn.execute(
                """
                INSERT OR REPLACE INTO memory_vectors
                    (key, value, source, importance, tags, related, embedding, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (key, value, source, level, tags_json, related_json,
                 embedding_blob, created_at, now),
            )

            # 同步 FTS（FTS5 用自己的列名，不受 rename 影响）
            conn.execute("DELETE FROM memory_fts WHERE key = ?", (key,))
            conn.execute(
                "INSERT INTO memory_fts (key, value, source, tags) VALUES (?, ?, ?, ?)",
                (key, value, source, fts_tags),
            )

            # Auto-detect contradictions and create links (Phase 4)
            self._auto_link_on_store_tx(conn, key, value, embedding_blob)

            # Set initial confidence based on source (Phase 5)
            self._set_initial_confidence_tx(conn, key, source, existing_confidence)

            # Initialize decay state (Phase 6)
            self._decay_init_tx(conn, key, source)

            # Auto-cluster into topics (Phase 7)
            if embedding_blob is not None:
                try:
                    self._auto_cluster_tx(conn, key, value, embedding_blob)
                except Exception:
                    pass

            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _auto_link_on_store_tx(self, conn, key: str, value: str,
                                embedding: bytes) -> None:
        """事务内版本：Auto-create supersedes and contradiction links after store()."""
        try:
            if embedding is not None:
                contradictions = self._detect_contradictions(key, embedding)
                for c in contradictions:
                    self._link_add_tx(conn, key, c["key"], "contradicts", c["similarity"])
        except Exception:
            pass  # link failures must not break store()

    def _link_add_tx(self, conn, from_key: str, to_key: str,
                     link_type: str, strength: float = 1.0) -> bool:
        """事务内版本：Add a typed link between two memories."""
        if link_type not in self.VALID_LINK_TYPES:
            return False
        # Avoid duplicates
        existing = conn.execute(
            "SELECT id FROM memory_links WHERE from_id = ? AND to_id = ? AND link_type = ?",
            (from_key, to_key, link_type),
        ).fetchone()
        if existing:
            return True
        now = int(time.time())
        conn.execute(
            "INSERT INTO memory_links (from_id, to_id, link_type, strength, created_at) VALUES (?, ?, ?, ?, ?)",
            (from_key, to_key, link_type, strength, now),
        )
        return True

    def _set_initial_confidence_tx(self, conn, key: str, source: str,
                                    existing_confidence: float = None) -> None:
        """事务内版本：Set confidence for a stored memory."""
        try:
            if existing_confidence is not None:
                conn.execute(
                    "UPDATE memory_vectors SET confidence = ? WHERE key = ?",
                    (existing_confidence, key),
                )
            else:
                conf = self._initial_confidence(source)
                conn.execute(
                    "UPDATE memory_vectors SET confidence = ? WHERE key = ? AND (confidence = 0.5 OR confidence IS NULL)",
                    (conf, key),
                )
        except Exception:
            pass

    def _decay_init_tx(self, conn, key: str, source: str = "") -> bool:
        """事务内版本：Initialize decay_state for a memory."""
        try:
            now = int(time.time())
            row = conn.execute(
                "SELECT source, importance FROM memory_vectors WHERE key = ?", (key,)
            ).fetchone()
            mem_source = row[0] if row else source
            mem_importance = row[1] if row else ""
            stability = self._base_stability(mem_source, mem_importance)
            conn.execute(
                """INSERT OR IGNORE INTO decay_state
                   (memory_key, difficulty, stability, retrievability, last_review)
                   VALUES (?, 0.0, ?, 1.0, ?)""",
                (key, stability, now),
            )
            return True
        except Exception:
            return False

    def _auto_cluster_tx(self, conn, key: str, value: str, embedding_blob: bytes) -> None:
        """事务内版本：Auto-cluster a memory into a topic."""
        # Convert blob to array for matching
        try:
            emb = np.frombuffer(embedding_blob, dtype=np.float32)
            if emb.shape[0] != self.EMBED_DIM:
                return
        except Exception:
            return

        topic_id, sim = self._topic_match_tx(conn, emb)
        if topic_id is not None:
            self._topic_add_memory_tx(conn, topic_id, key)
        else:
            name = value[:50].replace("\n", " ").strip()
            if not name:
                name = f"topic_{key}"
            topic_id = self._topic_create_tx(conn, name, embedding_blob)
            if topic_id > 0:
                self._topic_add_memory_tx(conn, topic_id, key)

        self._topic_counter += 1
        if self._topic_counter >= self.TOPIC_RECALC_INTERVAL:
            self._recalculate_all_topics()
            self._topic_counter = 0

    def _topic_match_tx(self, conn, embedding: np.ndarray) -> tuple:
        """事务内版本：Find best matching topic for an embedding."""
        try:
            rows = conn.execute(
                "SELECT id, centroid FROM topics WHERE centroid IS NOT NULL"
            ).fetchall()
            if not rows:
                return (None, 0.0)

            query_emb = np.asarray(embedding, dtype=np.float32).flatten()
            best_id = None
            best_sim = 0.0

            for topic_id, centroid_blob in rows:
                try:
                    centroid = np.frombuffer(centroid_blob, dtype=np.float32)
                    if centroid.shape[0] != self.EMBED_DIM:
                        continue
                    sim = float(np.dot(query_emb, centroid))
                    if sim > best_sim:
                        best_sim = sim
                        best_id = topic_id
                except Exception:
                    continue

            if best_sim >= self.TOPIC_MATCH_THRESHOLD:
                return (best_id, best_sim)
            return (None, best_sim)
        except Exception:
            return (None, 0.0)

    def _topic_create_tx(self, conn, name: str, centroid_blob: bytes) -> int:
        """事务内版本：Create a new topic. Returns topic id."""
        try:
            now = int(time.time())
            cur = conn.execute(
                "INSERT INTO topics (name, centroid, session_count, created_at) VALUES (?, ?, 0, ?)",
                (name, centroid_blob, now),
            )
            return cur.lastrowid
        except Exception:
            return -1

    def _topic_add_memory_tx(self, conn, topic_id: int, key: str) -> bool:
        """事务内版本：Link a memory to a topic."""
        try:
            now = int(time.time())
            conn.execute(
                "INSERT INTO session_topics (session_id, topic_id, similarity, created_at) VALUES (?, ?, 1.0, ?)",
                (key, topic_id, now),
            )
            conn.execute(
                "UPDATE topics SET session_count = session_count + 1 WHERE id = ?",
                (topic_id,),
            )
            return True
        except Exception:
            return False

    def search(self, query_emb: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        向量余弦相似度搜索。
        query_emb: shape (512,) 或 (1, 512) 的 float32 向量（已归一化）。
        返回 top_k 条结果，按相似度降序。
        """
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT key, value, source, importance, tags, related, embedding, created_at, updated_at "
                "FROM memory_vectors WHERE embedding IS NOT NULL"
            ).fetchall()

            if not rows:
                return []

            query_emb = np.asarray(query_emb, dtype=np.float32).flatten()

            results = []
            for row in rows:
                db_emb = np.frombuffer(row[6], dtype=np.float32)
                if db_emb.shape[0] != self.EMBED_DIM:
                    continue
                score = float(np.dot(query_emb, db_emb))
                results.append({
                    "key": row[0],
                    "value": row[1],
                    "source": row[2],
                    "importance": row[3],
                    "tags": row[4],
                    "related": json.loads(row[5]) if row[5] else [],
                    "created_at": row[7],
                    "updated_at": row[8],
                    "score": score,
                })

            results.sort(key=lambda x: x["score"], reverse=True)

            return results[:top_k]

        except Exception as e:
            print(f"[vmem] search error: {e}")
            return []

    def search_fts(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        FTS5 全文搜索，按 rank 排序（rank 值越小越相关，这里取负值方便与其他分数融合）。
        """
        try:
            conn = self._get_conn()
            rows = conn.execute(
                """
                SELECT m.key, m.value, m.source, m.importance, m.tags, m.related,
                       m.created_at, m.updated_at,
                       fts.rank
                FROM memory_fts AS fts
                JOIN memory_vectors AS m ON m.key = fts.key
                WHERE memory_fts MATCH ?
                ORDER BY fts.rank
                LIMIT ?
                """,
                (query, top_k),
            ).fetchall()

            results = []
            for row in rows:
                results.append({
                    "key": row[0],
                    "value": row[1],
                    "source": row[2],
                    "importance": row[3],
                    "tags": row[4],
                    "related": json.loads(row[5]) if row[5] else [],
                    "created_at": row[6],
                    "updated_at": row[7],
                    "score": -row[8],  # rank 越小越好，转为正分
                })

            return results

        except Exception as e:
            print(f"[vmem] search_fts error: {e}")
            return []

    def search_fusion(
        self,
        query: str,
        query_emb: np.ndarray,
        top_k: int = 10,
        w_vec: float = 0.50,
        w_fts: float = 0.20,
        w_time: float = 0.10,
        w_conf: float = 0.20,
        topic_filter: int = None,
    ) -> List[Dict[str, Any]]:
        """
        融合搜索：w_vec*向量 + w_fts*全文 + w_time*时间衰减 + w_conf*置信度。
        各分数归一化到 [0, 1] 后加权求和。
        """
        try:
            conn = self._get_conn()
            rows = conn.execute(
                """
                SELECT key, value, source, importance, tags, related, embedding,
                       created_at, updated_at, COALESCE(confidence, 0.5)
                FROM memory_vectors WHERE embedding IS NOT NULL
                """
            ).fetchall()

            if not rows:
                return []

            # Topic filter (Phase 7)
            if topic_filter is not None:
                topic_keys = {
                    r[0] for r in conn.execute(
                        "SELECT DISTINCT session_id FROM session_topics WHERE topic_id = ?",
                        (topic_filter,),
                    ).fetchall()
                }
                if topic_keys:
                    rows = [r for r in rows if r[0] in topic_keys]
                else:
                    return []

            query_emb = np.asarray(query_emb, dtype=np.float32).flatten()
            now = int(time.time())
            half_life = 7 * 24 * 3600  # 7 天半衰期

            # --- 向量得分 ---
            vec_scores = {}
            for row in rows:
                db_emb = np.frombuffer(row[6], dtype=np.float32)
                if db_emb.shape[0] != self.EMBED_DIM:
                    continue
                vec_scores[row[0]] = float(np.dot(query_emb, db_emb))

            # --- FTS 得分（从候选集中做 trigram 匹配）---
            fts_raw: Dict[str, float] = {}
            try:
                fts_rows = conn.execute(
                    """
                    SELECT key, rank FROM memory_fts
                    WHERE memory_fts MATCH ?
                    ORDER BY rank LIMIT 200
                    """,
                    (query,),
                ).fetchall()
                for key, rank in fts_rows:
                    fts_raw[key] = -rank  # rank 越小越好
            except Exception:
                pass  # trigram 可能匹配失败，忽略

            # --- 时间衰减得分 (Phase 6: FSRS retrievability) ---
            time_scores: Dict[str, float] = {}
            for row in rows:
                try:
                    r = self.decay_retrievability(row[0])
                    time_scores[row[0]] = r
                except Exception:
                    # Fallback to fixed half-life
                    updated_at = row[8] or row[7]
                    elapsed = max(now - updated_at, 0)
                    time_scores[row[0]] = 2 ** (-(elapsed / half_life))

            # --- 置信度得分 (Phase 5) ---
            conf_scores: Dict[str, float] = {}
            for row in rows:
                conf_scores[row[0]] = row[9]  # COALESCE(confidence, 0.5)

            # --- 归一化函数 ---
            def _normalize(d: Dict[str, float]) -> Dict[str, float]:
                if not d:
                    return {}
                vals = list(d.values())
                mn, mx = min(vals), max(vals)
                if mx - mn < 1e-9:
                    return {k: 0.5 for k in d}
                return {k: (v - mn) / (mx - mn) for k, v in d.items()}

            vec_norm = _normalize(vec_scores)
            fts_norm = _normalize(fts_raw)
            time_norm = _normalize(time_scores)
            conf_norm = _normalize(conf_scores)

            # --- 融合 ---
            all_keys = set()
            for d in (vec_norm, fts_norm, time_norm, conf_norm):
                all_keys.update(d.keys())

            fused = []
            for key in all_keys:
                s = (
                    w_vec * vec_norm.get(key, 0.0)
                    + w_fts * fts_norm.get(key, 0.0)
                    + w_time * time_norm.get(key, 0.0)
                    + w_conf * conf_norm.get(key, 0.0)
                )
                fused.append((key, s))

            fused.sort(key=lambda x: x[1], reverse=True)
            top_keys = [k for k, _ in fused[:top_k]]

            # 取回完整记录
            placeholders = ",".join("?" for _ in top_keys)
            full_rows = conn.execute(
                f"""
                SELECT key, value, source, importance, tags, related,
                       created_at, updated_at
                FROM memory_vectors WHERE key IN ({placeholders})
                """,
                top_keys,
            ).fetchall()

            row_map = {r[0]: r for r in full_rows}
            score_map = dict(fused)

            results = []
            for key in top_keys:
                r = row_map.get(key)
                if r is None:
                    continue
                results.append({
                    "key": r[0],
                    "value": r[1],
                    "source": r[2],
                    "importance": r[3],
                    "tags": r[4],
                    "related": json.loads(r[5]) if r[5] else [],
                    "created_at": r[6],
                    "updated_at": r[7],
                    "score": score_map.get(key, 0.0),
                })

            return results

        except Exception as e:
            print(f"[vmem] search_fusion error: {e}")
            return []

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """精确获取一条记忆。"""
        try:
            conn = self._get_conn()
            row = conn.execute(
                "SELECT key, value, source, importance, tags, related, created_at, updated_at "
                "FROM memory_vectors WHERE key = ?",
                (key,),
            ).fetchone()

            if row is None:
                return None

            return {
                "key": row[0],
                "value": row[1],
                "source": row[2],
                "importance": row[3],
                "tags": row[4],
                "related": json.loads(row[5]) if row[5] else [],
                "created_at": row[6],
                "updated_at": row[7],
            }

        except Exception as e:
            print(f"[vmem] get error: {e}")
            return None

    def delete(self, key: str) -> bool:
        """删除一条记忆（同时删除 FTS 索引）。"""
        try:
            conn = self._get_conn()
            conn.execute("DELETE FROM memory_vectors WHERE key = ?", (key,))
            conn.execute("DELETE FROM memory_fts WHERE key = ?", (key,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] delete error: {e}")
            return False

    def list_all(self, limit: int = 100, source_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出记忆，按更新时间降序。"""
        try:
            conn = self._get_conn()
            if source_filter:
                rows = conn.execute(
                    "SELECT key, value, source, importance, tags, related, created_at, updated_at "
                    "FROM memory_vectors WHERE source = ? ORDER BY updated_at DESC LIMIT ?",
                    (source_filter, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, value, source, importance, tags, related, created_at, updated_at "
                    "FROM memory_vectors ORDER BY updated_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()

            return [
                {
                    "key": r[0],
                    "value": r[1],
                    "source": r[2],
                    "importance": r[3],
                    "tags": r[4],
                    "related": json.loads(r[5]) if r[5] else [],
                    "created_at": r[6],
                    "updated_at": r[7],
                }
                for r in rows
            ]

        except Exception as e:
            print(f"[vmem] list_all error: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """返回存储统计信息。"""
        try:
            conn = self._get_conn()
            total = conn.execute("SELECT COUNT(*) FROM memory_vectors").fetchone()[0]
            sources = conn.execute(
                "SELECT source, COUNT(*) FROM memory_vectors GROUP BY source ORDER BY COUNT(*) DESC"
            ).fetchall()
            importance = conn.execute(
                "SELECT importance, COUNT(*) FROM memory_vectors GROUP BY importance ORDER BY COUNT(*) DESC"
            ).fetchall()

            oldest = conn.execute("SELECT MIN(created_at) FROM memory_vectors").fetchone()[0]
            newest = conn.execute("SELECT MAX(updated_at) FROM memory_vectors").fetchone()[0]

            return {
                "total": total,
                "sources": {s[0] or "(empty)": s[1] for s in sources},
                "importance": {l[0] or "(empty)": l[1] for l in importance},
                "oldest_created_at": oldest,
                "newest_updated_at": newest,
                "db_path": self._db_path,
            }

        except Exception as e:
            print(f"[vmem] get_stats error: {e}")
            return {"total": 0, "error": str(e)}

    # ------------------------------------------------------------------
    # 用户画像方法 (Phase 2: User Profile System)
    # ------------------------------------------------------------------

    def _ensure_default_profile(self) -> int:
        """Get or create the default user profile. Returns profile_id."""
        conn = self._get_conn()
        row = conn.execute(
            "SELECT id FROM user_profiles WHERE parent_id IS NULL LIMIT 1"
        ).fetchone()
        if row:
            return row[0]
        now = int(time.time())
        cur = conn.execute(
            "INSERT INTO user_profiles (parent_id, name, level, created_at) VALUES (NULL, 'default', 'root', ?)",
            (now,),
        )
        conn.commit()
        return cur.lastrowid

    def profile_set(
        self,
        attr_key: str,
        attr_value: str,
        category: str,
        confidence: float = 0.5,
        source: str = "auto",
    ) -> bool:
        """Upsert a profile attribute. Merges confidence via max(existing, new)."""
        try:
            conn = self._get_conn()
            profile_id = self._ensure_default_profile()
            now = int(time.time())

            existing = conn.execute(
                "SELECT id, confidence FROM profile_attributes WHERE profile_id = ? AND attr_key = ?",
                (profile_id, attr_key),
            ).fetchone()

            if existing:
                new_conf = max(existing[1], confidence)
                conn.execute(
                    "UPDATE profile_attributes SET attr_value = ?, confidence = ?, source = ?, updated_at = ? WHERE id = ?",
                    (attr_value, new_conf, source, now, existing[0]),
                )
            else:
                conn.execute(
                    "INSERT INTO profile_attributes (profile_id, attr_key, attr_value, category, confidence, source, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (profile_id, attr_key, attr_value, category, confidence, source, now),
                )

            # Sync FTS5 index (content-sync table needs explicit rebuild for trigram)
            conn.execute("INSERT INTO profile_attr_fts(profile_attr_fts) VALUES('rebuild')")
            conn.commit()
            return True

        except Exception as e:
            print(f"[vmem] profile_set error: {e}")
            return False

    def profile_get(self, attr_key: str = None, category: str = None) -> list:
        """Query profile attributes. Returns list of dicts with keys:
        attr_key, attr_value, category, confidence, source, updated_at"""
        try:
            conn = self._get_conn()
            profile_id = self._ensure_default_profile()

            if attr_key:
                rows = conn.execute(
                    "SELECT attr_key, attr_value, category, confidence, source, updated_at FROM profile_attributes WHERE profile_id = ? AND attr_key = ?",
                    (profile_id, attr_key),
                ).fetchall()
            elif category:
                rows = conn.execute(
                    "SELECT attr_key, attr_value, category, confidence, source, updated_at FROM profile_attributes WHERE profile_id = ? AND category = ? ORDER BY confidence DESC",
                    (profile_id, category),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT attr_key, attr_value, category, confidence, source, updated_at FROM profile_attributes WHERE profile_id = ? ORDER BY category, confidence DESC",
                    (profile_id,),
                ).fetchall()

            return [
                {
                    "attr_key": r[0],
                    "attr_value": r[1],
                    "category": r[2],
                    "confidence": r[3],
                    "source": r[4],
                    "updated_at": r[5],
                }
                for r in rows
            ]

        except Exception as e:
            print(f"[vmem] profile_get error: {e}")
            return []

    def profile_summary(self) -> str:
        """Generate markdown profile summary grouped by category.
        Returns '(no profile data)' if empty."""
        attrs = self.profile_get()
        if not attrs:
            return "(no profile data)"

        category_order = ["identity", "skills", "preferences", "tools", "efficiency", "projects"]
        grouped = {}
        for a in attrs:
            grouped.setdefault(a["category"], []).append(a)

        lines = []
        for cat in category_order:
            items = grouped.get(cat)
            if not items:
                continue
            lines.append(f"### {cat}")
            for item in items:
                line = f"- {item['attr_key']}: {item['attr_value']}"
                if item["confidence"] < 0.8:
                    line += f" ({item['confidence']:.0%})"
                lines.append(line)

        return "\n".join(lines) if lines else "(no profile data)"

    # ------------------------------------------------------------------
    # 因果链方法 (Phase 3: Causal Chain Memory)
    # ------------------------------------------------------------------

    VALID_RELATIONS = {"caused_by", "led_to", "resolved", "contradicts", "supersedes"}

    def causal_add(
        self,
        from_key: str,
        to_key: str,
        relation: str,
        strength: float = 1.0,
    ) -> bool:
        """Add a causal link and maintain closure_table."""
        if relation not in self.VALID_RELATIONS:
            print(f"[vmem] causal_add: invalid relation '{relation}'")
            return False
        try:
            conn = self._get_conn()
            now = int(time.time())

            conn.execute(
                "INSERT INTO causal_links (from_id, to_id, relation, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                (from_key, to_key, relation, strength, now),
            )

            # Maintain closure_table
            conn.execute(
                "INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth) VALUES (?, ?, 0)",
                (from_key, from_key),
            )
            conn.execute(
                "INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth) VALUES (?, ?, 0)",
                (to_key, to_key),
            )
            conn.execute(
                "INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth) VALUES (?, ?, 1)",
                (from_key, to_key),
            )
            # Transitive: ancestors of from_key → to_key
            conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT ct.ancestor, ?, ct.depth + 1
                   FROM closure_table ct
                   WHERE ct.descendant = ? AND ct.depth > 0""",
                (to_key, from_key),
            )
            # Transitive: from_key → descendants of to_key
            conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT ?, ct.descendant, ct.depth + 1
                   FROM closure_table ct
                   WHERE ct.ancestor = ? AND ct.depth > 0""",
                (from_key, to_key),
            )
            # Cross: ancestors of from_key → descendants of to_key
            conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT a.ancestor, d.descendant, a.depth + d.depth + 1
                   FROM closure_table a, closure_table d
                   WHERE a.descendant = ? AND a.depth > 0
                     AND d.ancestor = ? AND d.depth > 0""",
                (from_key, to_key),
            )

            conn.commit()
            return True

        except Exception as e:
            print(f"[vmem] causal_add error: {e}")
            return False

    def causal_chain(self, key: str, max_depth: int = 5) -> list:
        """Get causal chain ancestors for a key. Returns list of dicts."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                """SELECT ct.ancestor, ct.depth, mv.value, mv.source,
                          cl.relation, cl.strength
                   FROM closure_table ct
                   LEFT JOIN causal_links cl
                     ON (cl.from_id = ct.ancestor AND cl.to_id = ?)
                     OR (cl.to_id = ct.ancestor AND cl.from_id = ?)
                   LEFT JOIN memory_vectors mv ON mv.key = ct.ancestor
                   WHERE ct.descendant = ? AND ct.depth > 0 AND ct.depth <= ?
                   ORDER BY ct.depth""",
                (key, key, key, max_depth),
            ).fetchall()

            return [
                {
                    "key": r[0],
                    "depth": r[1],
                    "value": r[2] or "",
                    "source": r[3] or "",
                    "relation": r[4] or "",
                    "strength": r[5] or 0.0,
                }
                for r in rows
            ]

        except Exception as e:
            print(f"[vmem] causal_chain error: {e}")
            return []

    def causal_get(self, key: str) -> list:
        """Get all direct causal links where key is from_id or to_id."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT id, from_id, to_id, relation, strength, created_at FROM causal_links WHERE from_id = ? OR to_id = ?",
                (key, key),
            ).fetchall()
            return [
                {
                    "id": r[0],
                    "from_id": r[1],
                    "to_id": r[2],
                    "relation": r[3],
                    "strength": r[4],
                    "created_at": r[5],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[vmem] causal_get error: {e}")
            return []

    def causal_delete(self, link_id: int) -> bool:
        """Delete a causal link and rebuild closure_table."""
        try:
            conn = self._get_conn()

            link = conn.execute(
                "SELECT from_id, to_id FROM causal_links WHERE id = ?", (link_id,)
            ).fetchone()
            if not link:
                return False

            conn.execute("DELETE FROM causal_links WHERE id = ?", (link_id,))

            # Rebuild closure_table from remaining links
            conn.execute("DELETE FROM closure_table WHERE depth > 0")
            conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT from_id, from_id, 0 FROM causal_links
                   UNION
                   SELECT to_id, to_id, 0 FROM causal_links"""
            )
            conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT from_id, to_id, 1 FROM causal_links"""
            )
            # Iterative transitive closure
            for _ in range(10):
                result = conn.execute(
                    """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                       SELECT a.ancestor, d.descendant, a.depth + d.depth
                       FROM closure_table a
                       JOIN closure_table d ON a.descendant = d.ancestor AND d.depth > 0
                       WHERE a.depth > 0
                         AND NOT EXISTS (
                           SELECT 1 FROM closure_table e
                           WHERE e.ancestor = a.ancestor AND e.descendant = d.descendant
                         )"""
                )
                if result.rowcount == 0:
                    break

            conn.commit()
            return True

        except Exception as e:
            print(f"[vmem] causal_delete error: {e}")
            return False

    # ------------------------------------------------------------------
    # 记忆关系图方法 (Phase 4: Memory Relation Graph)
    # ------------------------------------------------------------------

    VALID_LINK_TYPES = {"related_to", "contradicts", "refines", "supersedes", "caused_by"}
    CONTRADICTION_THRESHOLD = 0.85

    def link_add(
        self,
        from_key: str,
        to_key: str,
        link_type: str,
        strength: float = 1.0,
    ) -> bool:
        """Add a typed link between two memories."""
        if link_type not in self.VALID_LINK_TYPES:
            print(f"[vmem] link_add: invalid link_type '{link_type}'")
            return False
        try:
            conn = self._get_conn()
            # Avoid duplicates
            existing = conn.execute(
                "SELECT id FROM memory_links WHERE from_id = ? AND to_id = ? AND link_type = ?",
                (from_key, to_key, link_type),
            ).fetchone()
            if existing:
                return True  # already exists

            now = int(time.time())
            conn.execute(
                "INSERT INTO memory_links (from_id, to_id, link_type, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                (from_key, to_key, link_type, strength, now),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] link_add error: {e}")
            return False

    def link_get(self, key: str, link_type: str = None) -> list:
        """Get all links involving a key, optionally filtered by type."""
        try:
            conn = self._get_conn()
            if link_type:
                rows = conn.execute(
                    "SELECT id, from_id, to_id, link_type, strength, created_at FROM memory_links WHERE (from_id = ? OR to_id = ?) AND link_type = ?",
                    (key, key, link_type),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id, from_id, to_id, link_type, strength, created_at FROM memory_links WHERE from_id = ? OR to_id = ?",
                    (key, key),
                ).fetchall()
            return [
                {
                    "id": r[0],
                    "from_id": r[1],
                    "to_id": r[2],
                    "link_type": r[3],
                    "strength": r[4],
                    "created_at": r[5],
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[vmem] link_get error: {e}")
            return []

    def link_delete(self, link_id: int) -> bool:
        """Delete a memory link."""
        try:
            conn = self._get_conn()
            conn.execute("DELETE FROM memory_links WHERE id = ?", (link_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] link_delete error: {e}")
            return False

    def _detect_contradictions(self, key: str, embedding: np.ndarray) -> list:
        """Find memories with high cosine similarity that may contradict."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT key, value, embedding FROM memory_vectors WHERE embedding IS NOT NULL AND key != ?",
                (key,),
            ).fetchall()

            query_emb = np.asarray(embedding, dtype=np.float32).flatten()
            contradictions = []
            for row in rows:
                try:
                    emb_data = row[2]
                    if emb_data is None:
                        continue
                    if not isinstance(emb_data, (bytes, bytearray, memoryview)):
                        continue
                    db_emb = np.frombuffer(bytes(emb_data), dtype=np.float32)
                    if db_emb.shape[0] != self.EMBED_DIM:
                        continue
                    sim = float(np.dot(query_emb, db_emb))
                    if sim >= self.CONTRADICTION_THRESHOLD:
                        contradictions.append({"key": row[0], "value": row[1], "similarity": sim})
                except Exception:
                    continue

            return contradictions
        except Exception as e:
            print(f"[vmem] _detect_contradictions error: {e}")
            return []

    def _auto_link_on_store(self, key: str, value: str, embedding: Optional[np.ndarray]) -> None:
        """Auto-create supersedes and contradiction links after store()."""
        try:
            # Contradiction detection
            if embedding is not None:
                contradictions = self._detect_contradictions(key, embedding)
                for c in contradictions:
                    self.link_add(key, c["key"], "contradicts", c["similarity"])
        except Exception:
            pass  # link failures must not break store()

    # ------------------------------------------------------------------
    # 置信度评分方法 (Phase 5: Confidence Scoring)
    # ------------------------------------------------------------------

    SOURCE_CONFIDENCE = {
        "user": 0.6, "user-explicit": 0.6,
        "lesson": 0.7, "auto-lesson": 0.7,
        "auto": 0.4, "auto-preference": 0.4,
    }

    def _initial_confidence(self, source: str) -> float:
        """Return initial confidence based on memory source."""
        return self.SOURCE_CONFIDENCE.get(source, 0.5)

    def confidence_update(self, key: str, delta: float, reason: str) -> bool:
        """Apply Bayesian confidence update and log the change."""
        try:
            conn = self._get_conn()
            now = int(time.time())

            row = conn.execute(
                "SELECT confidence FROM memory_vectors WHERE key = ?", (key,)
            ).fetchone()
            old_conf = row[0] if row else 0.5
            new_conf = max(0.0, min(1.0, old_conf + delta))

            conn.execute(
                "UPDATE memory_vectors SET confidence = ? WHERE key = ?",
                (new_conf, key),
            )
            conn.execute(
                "INSERT INTO confidence_log (memory_key, old_confidence, new_confidence, delta, reason, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (key, old_conf, new_conf, delta, reason, now),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] confidence_update error: {e}")
            return False

    def confidence_get(self, key: str) -> float:
        """Get current confidence for a memory key."""
        try:
            conn = self._get_conn()
            row = conn.execute(
                "SELECT confidence FROM memory_vectors WHERE key = ?", (key,)
            ).fetchone()
            return row[0] if row else 0.5
        except Exception:
            return 0.5

    def _set_initial_confidence(self, key: str, source: str, existing_confidence: float = None) -> None:
        """Set confidence for a stored memory. Preserves existing confidence if set."""
        try:
            conn = self._get_conn()
            if existing_confidence is not None:
                # Restore existing confidence after INSERT OR REPLACE
                conn.execute(
                    "UPDATE memory_vectors SET confidence = ? WHERE key = ?",
                    (existing_confidence, key),
                )
            else:
                # New entry: set based on source
                conf = self._initial_confidence(source)
                conn.execute(
                    "UPDATE memory_vectors SET confidence = ? WHERE key = ? AND (confidence = 0.5 OR confidence IS NULL)",
                    (conf, key),
                )
            conn.commit()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # FSRS 记忆衰减方法 (Phase 6: FSRS Memory Decay)
    # ------------------------------------------------------------------

    def _base_stability(self, source: str, importance: str = "") -> float:
        """Return base stability (in days) based on memory type."""
        combined = f"{source} {importance}".lower()
        if "error" in combined or "lesson" in combined:
            return 90.0
        if "preference" in combined or "profile" in combined:
            return 180.0
        if "session" in combined:
            return 7.0
        return 30.0

    def decay_init(self, key: str, source: str = "") -> bool:
        """Initialize decay_state for a memory with type-based stability."""
        try:
            conn = self._get_conn()
            now = int(time.time())

            # Get memory info for stability calculation
            row = conn.execute(
                "SELECT source, importance FROM memory_vectors WHERE key = ?", (key,)
            ).fetchone()
            mem_source = row[0] if row else source
            mem_importance = row[1] if row else ""

            stability = self._base_stability(mem_source, mem_importance)

            conn.execute(
                """INSERT OR IGNORE INTO decay_state
                   (memory_key, difficulty, stability, retrievability, last_review)
                   VALUES (?, 0.0, ?, 1.0, ?)""",
                (key, stability, now),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] decay_init error: {e}")
            return False

    def decay_recall(self, key: str) -> bool:
        """Reinforce memory on successful recall: stability += 10%."""
        try:
            conn = self._get_conn()
            now = int(time.time())

            row = conn.execute(
                "SELECT stability FROM decay_state WHERE memory_key = ?", (key,)
            ).fetchone()

            if not row:
                self.decay_init(key)
                row = conn.execute(
                    "SELECT stability FROM decay_state WHERE memory_key = ?", (key,)
                ).fetchone()

            if not row:
                return False

            new_stability = row[0] * 1.10
            conn.execute(
                "UPDATE decay_state SET stability = ?, last_review = ? WHERE memory_key = ?",
                (new_stability, now, key),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] decay_recall error: {e}")
            return False

    def decay_retrievability(self, key: str) -> float:
        """Calculate FSRS retrievability: R(t) = (1 + t/(9*S))^(-1)."""
        try:
            conn = self._get_conn()
            now = int(time.time())

            row = conn.execute(
                "SELECT stability, last_review FROM decay_state WHERE memory_key = ?", (key,)
            ).fetchone()

            if not row or not row[1]:
                return 1.0

            stability = row[0]
            last_review = row[1]
            t_days = max((now - last_review) / 86400.0, 0.0)

            if stability <= 0:
                return 0.01

            r = (1 + t_days / (9 * stability)) ** (-1)
            return max(r, 0.01)
        except Exception:
            return 1.0

    # ------------------------------------------------------------------
    # 话题聚类方法 (Phase 7: Cross-Session Topic Clustering)
    # ------------------------------------------------------------------

    TOPIC_MATCH_THRESHOLD = 0.75
    TOPIC_RECALC_INTERVAL = 50

    def topic_create(self, name: str, centroid: np.ndarray = None) -> int:
        """Create a new topic. Returns topic id."""
        try:
            conn = self._get_conn()
            now = int(time.time())
            centroid_blob = centroid.astype(np.float32).tobytes() if centroid is not None else None
            cur = conn.execute(
                "INSERT INTO topics (name, centroid, session_count, created_at) VALUES (?, ?, 0, ?)",
                (name, centroid_blob, now),
            )
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"[vmem] topic_create error: {e}")
            return -1

    def topic_match(self, embedding: np.ndarray) -> tuple:
        """Find best matching topic for an embedding. Returns (topic_id, similarity) or (None, 0)."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT id, centroid FROM topics WHERE centroid IS NOT NULL"
            ).fetchall()

            if not rows:
                return (None, 0.0)

            query_emb = np.asarray(embedding, dtype=np.float32).flatten()
            best_id = None
            best_sim = 0.0

            for topic_id, centroid_blob in rows:
                try:
                    centroid = np.frombuffer(centroid_blob, dtype=np.float32)
                    if centroid.shape[0] != self.EMBED_DIM:
                        continue
                    sim = float(np.dot(query_emb, centroid))
                    if sim > best_sim:
                        best_sim = sim
                        best_id = topic_id
                except Exception:
                    continue

            if best_sim >= self.TOPIC_MATCH_THRESHOLD:
                return (best_id, best_sim)
            return (None, best_sim)

        except Exception as e:
            print(f"[vmem] topic_match error: {e}")
            return (None, 0.0)

    def topic_add_memory(self, topic_id: int, key: str, session_id: str = "") -> bool:
        """Link a memory to a topic."""
        try:
            conn = self._get_conn()
            now = int(time.time())
            conn.execute(
                "INSERT INTO session_topics (session_id, topic_id, similarity, created_at) VALUES (?, ?, 1.0, ?)",
                (key, topic_id, now),  # Use key as session_id for memory linking
            )
            conn.execute(
                "UPDATE topics SET session_count = session_count + 1 WHERE id = ?",
                (topic_id,),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] topic_add_memory error: {e}")
            return False

    def topic_recalculate(self, topic_id: int) -> bool:
        """Recalculate topic centroid from linked memory embeddings."""
        try:
            conn = self._get_conn()

            # Get all memory keys linked to this topic
            keys = conn.execute(
                "SELECT DISTINCT session_id FROM session_topics WHERE topic_id = ?",
                (topic_id,),
            ).fetchall()

            embeddings = []
            for (key,) in keys:
                emb_row = conn.execute(
                    "SELECT embedding FROM memory_vectors WHERE key = ? AND embedding IS NOT NULL",
                    (key,),
                ).fetchone()
                if emb_row and emb_row[0]:
                    try:
                        emb_data = emb_row[0]
                        if not isinstance(emb_data, (bytes, bytearray, memoryview)):
                            continue
                        emb = np.frombuffer(bytes(emb_data), dtype=np.float32)
                        if emb.shape[0] == self.EMBED_DIM:
                            embeddings.append(emb.copy())
                    except Exception:
                        continue

            if not embeddings:
                return False

            mean_emb = np.mean(embeddings, axis=0).astype(np.float32)
            conn.execute(
                "UPDATE topics SET centroid = ? WHERE id = ?",
                (mean_emb.tobytes(), topic_id),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[vmem] topic_recalculate error: {e}")
            return False

    def topic_list(self) -> list:
        """List all topics."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT id, name, session_count, created_at FROM topics ORDER BY session_count DESC"
            ).fetchall()
            return [
                {"id": r[0], "name": r[1], "session_count": r[2], "created_at": r[3]}
                for r in rows
            ]
        except Exception:
            return []

    def _auto_cluster(self, key: str, value: str, embedding: np.ndarray) -> None:
        """Auto-cluster a memory into a topic."""
        topic_id, sim = self.topic_match(embedding)
        if topic_id is not None:
            self.topic_add_memory(topic_id, key)
        else:
            name = value[:50].replace("\n", " ").strip()
            if not name:
                name = f"topic_{key}"
            topic_id = self.topic_create(name, embedding)
            if topic_id > 0:
                self.topic_add_memory(topic_id, key)

        self._topic_counter += 1
        if self._topic_counter >= self.TOPIC_RECALC_INTERVAL:
            self._recalculate_all_topics()
            self._topic_counter = 0

    def _recalculate_all_topics(self) -> None:
        """Recalculate centroids for all topics."""
        try:
            topics = self.topic_list()
            for t in topics:
                self.topic_recalculate(t["id"])
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 自省方法 (Phase 8: Self-Reflection & Introspection)
    # ------------------------------------------------------------------

    def introspect_gc(self, max_age_days: int = 30, min_confidence: float = 0.2) -> list:
        """Mark low-confidence old memories as archived. Returns list of archived keys."""
        try:
            conn = self._get_conn()
            now = int(time.time())
            cutoff = now - max_age_days * 86400

            rows = conn.execute(
                """SELECT key FROM memory_vectors
                   WHERE confidence < ? AND updated_at < ? AND importance != 'archived'""",
                (min_confidence, cutoff),
            ).fetchall()

            archived_keys = [r[0] for r in rows]
            if archived_keys:
                conn.execute(
                    "UPDATE memory_vectors SET importance = 'archived' WHERE confidence < ? AND updated_at < ?",
                    (min_confidence, cutoff),
                )
                conn.commit()

            return archived_keys
        except Exception as e:
            print(f"[vmem] introspect_gc error: {e}")
            return []

    def introspect_contradictions(self, limit: int = 20) -> list:
        """Get recent contradiction links."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                """SELECT ml.from_id, ml.to_id, ml.strength,
                          mv1.value, mv2.value
                   FROM memory_links ml
                   LEFT JOIN memory_vectors mv1 ON mv1.key = ml.from_id
                   LEFT JOIN memory_vectors mv2 ON mv2.key = ml.to_id
                   WHERE ml.link_type = 'contradicts'
                   ORDER BY ml.created_at DESC
                   LIMIT ?""",
                (limit,),
            ).fetchall()
            return [
                {
                    "from_key": r[0],
                    "to_key": r[1],
                    "strength": r[2],
                    "from_value": r[3] or "",
                    "to_value": r[4] or "",
                }
                for r in rows
            ]
        except Exception as e:
            print(f"[vmem] introspect_contradictions error: {e}")
            return []

    def introspect_health(self) -> dict:
        """Return system health report."""
        try:
            conn = self._get_conn()
            now = int(time.time())
            cutoff_30d = now - 30 * 86400

            total = conn.execute("SELECT COUNT(*) FROM memory_vectors").fetchone()[0]
            topics = conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
            avg_conf = conn.execute("SELECT AVG(confidence) FROM memory_vectors").fetchone()[0] or 0.0
            gc_candidates = conn.execute(
                "SELECT COUNT(*) FROM memory_vectors WHERE confidence < 0.2 AND updated_at < ?",
                (cutoff_30d,),
            ).fetchone()[0]
            contradictions = conn.execute(
                "SELECT COUNT(*) FROM memory_links WHERE link_type = 'contradicts'"
            ).fetchone()[0]
            causal_chains = conn.execute("SELECT COUNT(*) FROM causal_links").fetchone()[0]
            profile_attrs = conn.execute("SELECT COUNT(*) FROM profile_attributes").fetchone()[0]
            archived = conn.execute(
                "SELECT COUNT(*) FROM memory_vectors WHERE importance = 'archived'"
            ).fetchone()[0]

            return {
                "total_memories": total,
                "total_topics": topics,
                "avg_confidence": round(avg_conf, 3),
                "gc_candidates": gc_candidates,
                "contradictions": contradictions,
                "causal_chains": causal_chains,
                "profile_attributes": profile_attrs,
                "archived": archived,
            }
        except Exception as e:
            print(f"[vmem] introspect_health error: {e}")
            return {"error": str(e)}

    # ------------------------------------------------------------------
    # 快照与恢复 (Snapshot & Restore)
    # ------------------------------------------------------------------

    def snapshot_export(self, output_path: str) -> Dict[str, Any]:
        """
        Export all memory data to a JSON snapshot file.

        Exports memory_vectors (with base64-encoded embeddings), causal_links,
        memory_links, topics (with base64-encoded centroids), and session_topics.

        The file includes metadata: export timestamp, record count, and schema
        version (latest migration name from schema_migrations).

        Returns a dict with summary info (record_count, path, schema_version).
        """
        conn = self._get_conn()

        # --- memory_vectors ---
        rows = conn.execute(
            "SELECT key, value, source, importance, tags, related, embedding, "
            "confidence, created_at, updated_at FROM memory_vectors"
        ).fetchall()

        memory_vectors = []
        for r in rows:
            emb_b64 = base64.b64encode(r[6]).decode("ascii") if r[6] is not None else None
            memory_vectors.append({
                "key": r[0],
                "value": r[1],
                "source": r[2],
                "importance": r[3],
                "tags": r[4],
                "related": r[5],
                "embedding_b64": emb_b64,
                "confidence": r[7],
                "created_at": r[8],
                "updated_at": r[9],
            })

        # --- causal_links ---
        causal_rows = conn.execute(
            "SELECT id, from_id, to_id, relation, strength, created_at FROM causal_links"
        ).fetchall()
        causal_links = [
            {"id": r[0], "from_id": r[1], "to_id": r[2],
             "relation": r[3], "strength": r[4], "created_at": r[5]}
            for r in causal_rows
        ]

        # --- memory_links ---
        link_rows = conn.execute(
            "SELECT id, from_id, to_id, link_type, strength, created_at FROM memory_links"
        ).fetchall()
        memory_links = [
            {"id": r[0], "from_id": r[1], "to_id": r[2],
             "link_type": r[3], "strength": r[4], "created_at": r[5]}
            for r in link_rows
        ]

        # --- topics (centroid is BLOB, base64 encode) ---
        topic_rows = conn.execute(
            "SELECT id, name, centroid, session_count, created_at FROM topics"
        ).fetchall()
        topics = []
        for r in topic_rows:
            centroid_b64 = base64.b64encode(r[2]).decode("ascii") if r[2] is not None else None
            topics.append({
                "id": r[0],
                "name": r[1],
                "centroid_b64": centroid_b64,
                "session_count": r[3],
                "created_at": r[4],
            })

        # --- session_topics ---
        st_rows = conn.execute(
            "SELECT id, session_id, topic_id, similarity, created_at FROM session_topics"
        ).fetchall()
        session_topics = [
            {"id": r[0], "session_id": r[1], "topic_id": r[2],
             "similarity": r[3], "created_at": r[4]}
            for r in st_rows
        ]

        # --- schema version: latest applied migration ---
        latest_version = None
        try:
            row = conn.execute(
                "SELECT migration_name FROM schema_migrations ORDER BY migration_name DESC LIMIT 1"
            ).fetchone()
            if row:
                latest_version = row[0]
        except Exception:
            pass

        snapshot = {
            "meta": {
                "exported_at": int(time.time()),
                "record_count": len(memory_vectors),
                "schema_version": latest_version,
            },
            "memory_vectors": memory_vectors,
            "causal_links": causal_links,
            "memory_links": memory_links,
            "topics": topics,
            "session_topics": session_topics,
        }

        # Write to file
        output_path = str(output_path)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        return {
            "path": output_path,
            "record_count": len(memory_vectors),
            "causal_link_count": len(causal_links),
            "memory_link_count": len(memory_links),
            "topic_count": len(topics),
            "session_topic_count": len(session_topics),
            "schema_version": latest_version,
        }

    def snapshot_import(self, json_path: str, mode: str = "merge") -> Dict[str, Any]:
        """
        Import memory data from a JSON snapshot file.

        Args:
            json_path: Path to the snapshot JSON file.
            mode: Import strategy:
                - "merge": Skip records whose key already exists (default).
                - "overwrite": Clear all data first, then import everything.
                - "upsert": For each key, keep the record with the newer
                            updated_at timestamp.

        Returns a dict with import statistics.

        After import, FTS5 index is rebuilt and migrations are re-run to
        ensure schema compatibility.
        """
        if mode not in ("merge", "overwrite", "upsert"):
            raise ValueError(f"Invalid mode '{mode}'. Must be merge, overwrite, or upsert.")

        # Read and parse snapshot file
        json_path = str(json_path)
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                snapshot = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Snapshot file not found: {json_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in snapshot file: {e}")

        if not isinstance(snapshot, dict) or "memory_vectors" not in snapshot:
            raise ValueError("Snapshot file missing 'memory_vectors' field.")

        conn = self._get_conn()

        memory_vectors = snapshot.get("memory_vectors", [])
        causal_links = snapshot.get("causal_links", [])
        memory_links = snapshot.get("memory_links", [])
        topics = snapshot.get("topics", [])
        session_topics = snapshot.get("session_topics", [])

        stats = {
            "imported": 0,
            "skipped": 0,
            "overwritten": 0,
            "causal_links_imported": 0,
            "memory_links_imported": 0,
            "topics_imported": 0,
            "session_topics_imported": 0,
            "mode": mode,
        }

        try:
            # --- mode=overwrite: clear all data first ---
            if mode == "overwrite":
                conn.execute("DELETE FROM session_topics")
                conn.execute("DELETE FROM topics")
                conn.execute("DELETE FROM memory_links")
                conn.execute("DELETE FROM causal_links")
                conn.execute("DELETE FROM closure_table")
                conn.execute("DELETE FROM memory_fts")
                conn.execute("DELETE FROM memory_vectors")

            # --- import memory_vectors ---
            existing_keys = set()
            existing_updated = {}
            if mode != "overwrite":
                rows = conn.execute(
                    "SELECT key, updated_at FROM memory_vectors"
                ).fetchall()
                for r in rows:
                    existing_keys.add(r[0])
                    existing_updated[r[0]] = r[1]

            for rec in memory_vectors:
                key = rec.get("key")
                if not key:
                    continue

                # Decode embedding
                emb_b64 = rec.get("embedding_b64")
                embedding = base64.b64decode(emb_b64) if emb_b64 else None

                value = rec.get("value", "")
                source = rec.get("source", "")
                importance = rec.get("importance", "")
                tags = rec.get("tags", "[]")
                related = rec.get("related", "[]")
                confidence = rec.get("confidence", 0.5)
                created_at = rec.get("created_at", int(time.time()))
                updated_at = rec.get("updated_at", int(time.time()))

                if mode == "overwrite":
                    # Full import — just insert
                    conn.execute(
                        """INSERT INTO memory_vectors
                           (key, value, source, importance, tags, related, embedding,
                            confidence, created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (key, value, source, importance, tags, related, embedding,
                         confidence, created_at, updated_at),
                    )
                    stats["imported"] += 1

                elif mode == "merge":
                    # Skip existing keys
                    if key in existing_keys:
                        stats["skipped"] += 1
                        continue
                    conn.execute(
                        """INSERT INTO memory_vectors
                           (key, value, source, importance, tags, related, embedding,
                            confidence, created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (key, value, source, importance, tags, related, embedding,
                         confidence, created_at, updated_at),
                    )
                    stats["imported"] += 1

                elif mode == "upsert":
                    # Keep the newer record by updated_at
                    if key in existing_keys:
                        if updated_at > existing_updated[key]:
                            conn.execute(
                                """UPDATE memory_vectors SET
                                   value = ?, source = ?, importance = ?, tags = ?,
                                   related = ?, embedding = ?, confidence = ?,
                                   created_at = ?, updated_at = ?
                                   WHERE key = ?""",
                                (value, source, importance, tags, related, embedding,
                                 confidence, created_at, updated_at, key),
                            )
                            stats["overwritten"] += 1
                        else:
                            stats["skipped"] += 1
                    else:
                        conn.execute(
                            """INSERT INTO memory_vectors
                               (key, value, source, importance, tags, related, embedding,
                                confidence, created_at, updated_at)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (key, value, source, importance, tags, related, embedding,
                             confidence, created_at, updated_at),
                        )
                        stats["imported"] += 1

            # --- rebuild FTS5 index ---
            conn.execute("DELETE FROM memory_fts")
            fts_rows = conn.execute(
                "SELECT key, value, source, tags FROM memory_vectors"
            ).fetchall()
            for r in fts_rows:
                # For FTS, convert tags JSON back to comma-separated for trigram matching
                tags_str = r[3] or ""
                try:
                    tag_list = json.loads(tags_str)
                    if isinstance(tag_list, list):
                        tags_str = ",".join(tag_list)
                except (json.JSONDecodeError, TypeError):
                    pass  # keep as-is
                conn.execute(
                    "INSERT INTO memory_fts (key, value, source, tags) VALUES (?, ?, ?, ?)",
                    (r[0], r[1], r[2], tags_str),
                )

            # --- import topics ---
            if mode == "overwrite":
                for t in topics:
                    centroid = base64.b64decode(t["centroid_b64"]) if t.get("centroid_b64") else None
                    conn.execute(
                        """INSERT INTO topics (id, name, centroid, session_count, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (t.get("id"), t.get("name", ""), centroid,
                         t.get("session_count", 0), t.get("created_at", int(time.time()))),
                    )
                    stats["topics_imported"] += 1
            else:
                # For merge/upsert: only import topics that don't exist by id
                existing_topic_ids = {
                    r[0] for r in conn.execute("SELECT id FROM topics").fetchall()
                }
                for t in topics:
                    tid = t.get("id")
                    if tid in existing_topic_ids:
                        continue
                    centroid = base64.b64decode(t["centroid_b64"]) if t.get("centroid_b64") else None
                    conn.execute(
                        """INSERT INTO topics (id, name, centroid, session_count, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (tid, t.get("name", ""), centroid,
                         t.get("session_count", 0), t.get("created_at", int(time.time()))),
                    )
                    stats["topics_imported"] += 1

            # --- import session_topics ---
            if mode == "overwrite":
                for st in session_topics:
                    conn.execute(
                        """INSERT INTO session_topics
                           (id, session_id, topic_id, similarity, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (st.get("id"), st.get("session_id", ""), st.get("topic_id", 0),
                         st.get("similarity", 0.0), st.get("created_at", int(time.time()))),
                    )
                    stats["session_topics_imported"] += 1
            else:
                # For merge/upsert: skip by (session_id, topic_id) to avoid duplicates
                existing_st_pairs = {
                    (r[0], r[1])
                    for r in conn.execute(
                        "SELECT session_id, topic_id FROM session_topics"
                    ).fetchall()
                }
                for st in session_topics:
                    pair = (st.get("session_id", ""), st.get("topic_id", 0))
                    if pair in existing_st_pairs:
                        continue
                    conn.execute(
                        """INSERT INTO session_topics
                           (session_id, topic_id, similarity, created_at)
                           VALUES (?, ?, ?, ?)""",
                        (st.get("session_id", ""), st.get("topic_id", 0),
                         st.get("similarity", 0.0), st.get("created_at", int(time.time()))),
                    )
                    stats["session_topics_imported"] += 1

            # --- import causal_links ---
            if mode == "overwrite":
                for cl in causal_links:
                    conn.execute(
                        """INSERT INTO causal_links
                           (from_id, to_id, relation, strength, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (cl.get("from_id", ""), cl.get("to_id", ""),
                         cl.get("relation", ""), cl.get("strength", 1.0),
                         cl.get("created_at", int(time.time()))),
                    )
                    stats["causal_links_imported"] += 1
                # Rebuild closure_table for overwrite mode
                self._rebuild_closure_table(conn)
            else:
                # For merge/upsert: skip duplicate (from_id, to_id, relation) triples
                existing_cl = {
                    (r[0], r[1], r[2])
                    for r in conn.execute(
                        "SELECT from_id, to_id, relation FROM causal_links"
                    ).fetchall()
                }
                for cl in causal_links:
                    triple = (cl.get("from_id", ""), cl.get("to_id", ""), cl.get("relation", ""))
                    if triple in existing_cl:
                        continue
                    conn.execute(
                        """INSERT INTO causal_links
                           (from_id, to_id, relation, strength, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (cl.get("from_id", ""), cl.get("to_id", ""),
                         cl.get("relation", ""), cl.get("strength", 1.0),
                         cl.get("created_at", int(time.time()))),
                    )
                    stats["causal_links_imported"] += 1
                # Rebuild closure_table incrementally not needed — full rebuild is safer
                if stats["causal_links_imported"] > 0:
                    self._rebuild_closure_table(conn)

            # --- import memory_links ---
            if mode == "overwrite":
                for ml in memory_links:
                    conn.execute(
                        """INSERT INTO memory_links
                           (from_id, to_id, link_type, strength, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (ml.get("from_id", ""), ml.get("to_id", ""),
                         ml.get("link_type", ""), ml.get("strength", 1.0),
                         ml.get("created_at", int(time.time()))),
                    )
                    stats["memory_links_imported"] += 1
            else:
                # For merge/upsert: skip duplicate (from_id, to_id, link_type)
                existing_ml = {
                    (r[0], r[1], r[2])
                    for r in conn.execute(
                        "SELECT from_id, to_id, link_type FROM memory_links"
                    ).fetchall()
                }
                for ml in memory_links:
                    triple = (ml.get("from_id", ""), ml.get("to_id", ""), ml.get("link_type", ""))
                    if triple in existing_ml:
                        continue
                    conn.execute(
                        """INSERT INTO memory_links
                           (from_id, to_id, link_type, strength, created_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        (ml.get("from_id", ""), ml.get("to_id", ""),
                         ml.get("link_type", ""), ml.get("strength", 1.0),
                         ml.get("created_at", int(time.time()))),
                    )
                    stats["memory_links_imported"] += 1

            conn.commit()

            # --- run migrations to ensure schema compatibility ---
            from vmem.migrations import run_migrations
            run_migrations(conn)

            return stats

        except Exception:
            conn.rollback()
            raise

    def _rebuild_closure_table(self, conn: sqlite3.Connection) -> None:
        """Rebuild closure_table from all causal_links."""
        conn.execute("DELETE FROM closure_table")
        # Self-references (depth 0)
        conn.execute(
            """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
               SELECT from_id, from_id, 0 FROM causal_links
               UNION
               SELECT to_id, to_id, 0 FROM causal_links"""
        )
        # Direct links (depth 1)
        conn.execute(
            """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
               SELECT from_id, to_id, 1 FROM causal_links"""
        )
        # Iterative transitive closure
        for _ in range(10):
            result = conn.execute(
                """INSERT OR IGNORE INTO closure_table (ancestor, descendant, depth)
                   SELECT a.ancestor, d.descendant, a.depth + d.depth
                   FROM closure_table a
                   JOIN closure_table d ON a.descendant = d.ancestor AND d.depth > 0
                   WHERE a.depth > 0
                     AND NOT EXISTS (
                       SELECT 1 FROM closure_table e
                       WHERE e.ancestor = a.ancestor AND e.descendant = d.descendant
                     )"""
            )
            if result.rowcount == 0:
                break

    # ------------------------------------------------------------------
    # 记忆去重与智能合并 (Phase 9: Deduplication & Smart Merge)
    # ------------------------------------------------------------------

    def find_duplicates(self, threshold: float = 0.92, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """
        基于向量余弦相似度查找重复记忆对。

        使用 numpy 矩阵运算批量计算相似度。当记录数超过 10000 时，
        采用分块（chunk_size=1000）策略以控制内存使用。

        Args:
            threshold: 相似度阈值，默认 0.92（高于此值视为重复）。
            chunk_size: 分块大小，默认 1000。仅当总记录数 > 10000 时分块生效。

        Returns:
            List of dicts: [{"key_a": str, "key_b": str, "similarity": float}, ...]
            每对只出现一次（按 key 字典序排序，key_a < key_b）。
        """
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT key, embedding FROM memory_vectors WHERE embedding IS NOT NULL"
            ).fetchall()

            if len(rows) < 2:
                return []

            # 收集所有 key 和 embedding
            keys = []
            embeddings = []
            for key, emb_blob in rows:
                try:
                    emb = np.frombuffer(emb_blob, dtype=np.float32)
                    if emb.shape[0] != self.EMBED_DIM:
                        continue
                    keys.append(key)
                    embeddings.append(emb)
                except Exception:
                    continue

            n = len(keys)
            if n < 2:
                return []

            emb_matrix = np.stack(embeddings).astype(np.float32)  # shape: (n, 512)

            # 小数据集：直接全矩阵运算
            if n <= 10000:
                # 归一化向量已在 encode 时完成，cosine = dot product
                sim_matrix = emb_matrix @ emb_matrix.T  # shape: (n, n)

                # 获取上三角（不含对角线）的高相似度对
                iu = np.triu_indices(n, k=1)
                sims = sim_matrix[iu]
                mask = sims >= threshold

                i_indices = iu[0][mask]
                j_indices = iu[1][mask]
                sim_values = sims[mask]

                results = []
                for i, j, s in zip(i_indices, j_indices, sim_values):
                    ka, kb = keys[i], keys[j]
                    # 按字典序排序确保 key_a < key_b
                    if ka > kb:
                        ka, kb = kb, ka
                    results.append({
                        "key_a": ka,
                        "key_b": kb,
                        "similarity": float(s),
                    })

                # 按相似度降序排序
                results.sort(key=lambda x: x["similarity"], reverse=True)
                return results

            # 大数据集：分块计算以控制内存
            results = []
            for i_start in range(0, n, chunk_size):
                i_end = min(i_start + chunk_size, n)
                chunk_i = emb_matrix[i_start:i_end]  # shape: (chunk_i_size, 512)

                for j_start in range(i_start + 1, n, chunk_size):
                    j_end = min(j_start + chunk_size, n)
                    chunk_j = emb_matrix[j_start:j_end]  # shape: (chunk_j_size, 512)

                    # 块间相似度矩阵
                    sim_block = chunk_i @ chunk_j.T  # shape: (chunk_i_size, chunk_j_size)

                    # 找出高相似度对
                    above = np.argwhere(sim_block >= threshold)
                    for ii, jj in above:
                        global_i = i_start + ii
                        global_j = j_start + jj
                        ka, kb = keys[global_i], keys[global_j]
                        if ka > kb:
                            ka, kb = kb, ka
                        results.append({
                            "key_a": ka,
                            "key_b": kb,
                            "similarity": float(sim_block[ii, jj]),
                        })

            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results

        except Exception as e:
            print(f"[vmem] find_duplicates error: {e}")
            return []

    def merge_memories(
        self,
        key_a: str,
        key_b: str,
        strategy: str = "keep_richer",
    ) -> Dict[str, Any]:
        """
        合并两条记忆，保留一条作为幸存者，另一条被删除。

        Args:
            key_a: 第一条记忆的 key。
            key_b: 第二条记忆的 key。
            strategy: 合并策略：
                - "keep_richer": 保留信息更丰富的那条（默认）
                  评估维度：value 长度、tags 数量、关联链接数
                - "keep_newer": 保留 updated_at 较新的那条
                - "manual": 以 key_a 为幸存者，合并 key_b 的部分信息

        Returns:
            dict with keys: {survivor_key, merged_key, strategy,
                             old_confidence, new_confidence,
                             links_transferred, causal_transferred}
        """
        if strategy not in ("keep_richer", "keep_newer", "manual"):
            raise ValueError(
                f"Invalid strategy '{strategy}'. "
                "Must be 'keep_richer', 'keep_newer', or 'manual'."
            )

        try:
            conn = self._get_conn()

            # 获取两条记忆的完整信息
            row_a = conn.execute(
                "SELECT key, value, source, importance, tags, related, "
                "confidence, created_at, updated_at "
                "FROM memory_vectors WHERE key = ?",
                (key_a,),
            ).fetchone()
            row_b = conn.execute(
                "SELECT key, value, source, importance, tags, related, "
                "confidence, created_at, updated_at "
                "FROM memory_vectors WHERE key = ?",
                (key_b,),
            ).fetchone()

            if row_a is None or row_b is None:
                return {"error": "One or both keys not found"}

            mem_a = {
                "key": row_a[0], "value": row_a[1], "source": row_a[2],
                "importance": row_a[3], "tags": row_a[4], "related": row_a[5],
                "confidence": row_a[6] or 0.5,
                "created_at": row_a[7], "updated_at": row_a[8],
            }
            mem_b = {
                "key": row_b[0], "value": row_b[1], "source": row_b[2],
                "importance": row_b[3], "tags": row_b[4], "related": row_b[5],
                "confidence": row_b[6] or 0.5,
                "created_at": row_b[7], "updated_at": row_b[8],
            }

            # 计算 richness 分数
            def _richness(mem: dict) -> float:
                score = 0.0
                score += len(mem["value"]) * 0.01  # value 长度
                try:
                    tag_list = json.loads(mem["tags"]) if mem["tags"] else []
                    if isinstance(tag_list, list):
                        score += len(tag_list) * 5
                except Exception:
                    pass
                try:
                    rel_list = json.loads(mem["related"]) if mem["related"] else []
                    if isinstance(rel_list, list):
                        score += len(rel_list) * 3
                except Exception:
                    pass
                score += mem["confidence"] * 10
                return score

            # 确定幸存者
            if strategy == "keep_richer":
                if _richness(mem_a) >= _richness(mem_b):
                    survivor, merged = mem_a, mem_b
                else:
                    survivor, merged = mem_b, mem_a
            elif strategy == "keep_newer":
                if mem_a["updated_at"] >= mem_b["updated_at"]:
                    survivor, merged = mem_a, mem_b
                else:
                    survivor, merged = mem_b, mem_a
            else:  # manual
                survivor, merged = mem_a, mem_b

            survivor_key = survivor["key"]
            merged_key = merged["key"]

            old_confidence = survivor["confidence"]

            # 置信度提升 10%（上限 1.0）
            new_confidence = min(survivor["confidence"] * 1.10, 1.0)

            # 合并 tags（去重）
            try:
                surv_tags = json.loads(survivor["tags"]) if survivor["tags"] else []
                if not isinstance(surv_tags, list):
                    surv_tags = []
            except Exception:
                surv_tags = []
            try:
                merged_tags = json.loads(merged["tags"]) if merged["tags"] else []
                if not isinstance(merged_tags, list):
                    merged_tags = []
            except Exception:
                merged_tags = []

            combined_tags = list(dict.fromkeys(surv_tags + merged_tags))
            new_tags_json = json.dumps(combined_tags, ensure_ascii=False)

            # 合并 related（去重）
            try:
                surv_rel = json.loads(survivor["related"]) if survivor["related"] else []
                if not isinstance(surv_rel, list):
                    surv_rel = []
            except Exception:
                surv_rel = []
            try:
                merged_rel = json.loads(merged["related"]) if merged["related"] else []
                if not isinstance(merged_rel, list):
                    merged_rel = []
            except Exception:
                merged_rel = []

            combined_rel = list(dict.fromkeys(surv_rel + merged_rel))
            # 移除幸存者自身的 key
            combined_rel = [k for k in combined_rel if k != survivor_key and k != merged_key]
            new_rel_json = json.dumps(combined_rel, ensure_ascii=False)

            # value 合并策略：取较长的那个（richer 策略的补充）
            # 如果幸存者的 value 明显更短，追加 merged 的 value
            new_value = survivor["value"]
            if len(merged["value"]) > len(survivor["value"]) * 1.5:
                new_value = survivor["value"] + "\n\n" + merged["value"]

            now = int(time.time())

            # 开始事务
            conn.execute("BEGIN IMMEDIATE")
            try:
                # 更新幸存者
                conn.execute(
                    """UPDATE memory_vectors SET
                           value = ?, tags = ?, related = ?,
                           confidence = ?, updated_at = ?
                       WHERE key = ?""",
                    (new_value, new_tags_json, new_rel_json,
                     new_confidence, now, survivor_key),
                )

                # 转移 causal_links：merged → survivor
                # 1. merged 作为 from_id 的链接
                causal_from = conn.execute(
                    "SELECT to_id, relation, strength FROM causal_links WHERE from_id = ?",
                    (merged_key,),
                ).fetchall()
                causal_transferred = 0
                for to_id, relation, strength in causal_from:
                    if to_id == survivor_key:
                        continue  # 跳过自引用
                    # 检查是否已存在
                    existing = conn.execute(
                        "SELECT id FROM causal_links WHERE from_id = ? AND to_id = ? AND relation = ?",
                        (survivor_key, to_id, relation),
                    ).fetchone()
                    if not existing:
                        conn.execute(
                            "INSERT INTO causal_links (from_id, to_id, relation, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                            (survivor_key, to_id, relation, strength, now),
                        )
                        causal_transferred += 1

                # 2. merged 作为 to_id 的链接
                causal_to = conn.execute(
                    "SELECT from_id, relation, strength FROM causal_links WHERE to_id = ?",
                    (merged_key,),
                ).fetchall()
                for from_id, relation, strength in causal_to:
                    if from_id == survivor_key:
                        continue
                    existing = conn.execute(
                        "SELECT id FROM causal_links WHERE from_id = ? AND to_id = ? AND relation = ?",
                        (from_id, survivor_key, relation),
                    ).fetchone()
                    if not existing:
                        conn.execute(
                            "INSERT INTO causal_links (from_id, to_id, relation, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                            (from_id, survivor_key, relation, strength, now),
                        )
                        causal_transferred += 1

                # 删除 merged 的 causal_links
                conn.execute(
                    "DELETE FROM causal_links WHERE from_id = ? OR to_id = ?",
                    (merged_key, merged_key),
                )

                # 转移 memory_links：merged → survivor
                links_transferred = 0

                # 1. merged 作为 from_id
                link_from = conn.execute(
                    "SELECT to_id, link_type, strength FROM memory_links WHERE from_id = ?",
                    (merged_key,),
                ).fetchall()
                for to_id, link_type, strength in link_from:
                    if to_id == survivor_key:
                        continue
                    existing = conn.execute(
                        "SELECT id FROM memory_links WHERE from_id = ? AND to_id = ? AND link_type = ?",
                        (survivor_key, to_id, link_type),
                    ).fetchone()
                    if not existing:
                        conn.execute(
                            "INSERT INTO memory_links (from_id, to_id, link_type, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                            (survivor_key, to_id, link_type, strength, now),
                        )
                        links_transferred += 1

                # 2. merged 作为 to_id
                link_to = conn.execute(
                    "SELECT from_id, link_type, strength FROM memory_links WHERE to_id = ?",
                    (merged_key,),
                ).fetchall()
                for from_id, link_type, strength in link_to:
                    if from_id == survivor_key:
                        continue
                    existing = conn.execute(
                        "SELECT id FROM memory_links WHERE from_id = ? AND to_id = ? AND link_type = ?",
                        (from_id, survivor_key, link_type),
                    ).fetchone()
                    if not existing:
                        conn.execute(
                            "INSERT INTO memory_links (from_id, to_id, link_type, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                            (from_id, survivor_key, link_type, strength, now),
                        )
                        links_transferred += 1

                # 删除 merged 的 memory_links
                conn.execute(
                    "DELETE FROM memory_links WHERE from_id = ? OR to_id = ?",
                    (merged_key, merged_key),
                )

                # 删除 merged 在 session_topics 中的记录
                conn.execute(
                    "DELETE FROM session_topics WHERE session_id = ?",
                    (merged_key,),
                )

                # 删除 merged 的 decay_state
                conn.execute(
                    "DELETE FROM decay_state WHERE memory_key = ?",
                    (merged_key,),
                )

                # 删除 merged 的 FTS 记录
                conn.execute("DELETE FROM memory_fts WHERE key = ?", (merged_key,))

                # 更新幸存者的 FTS 记录
                conn.execute("DELETE FROM memory_fts WHERE key = ?", (survivor_key,))
                fts_tags = ",".join(combined_tags)
                conn.execute(
                    "INSERT INTO memory_fts (key, value, source, tags) VALUES (?, ?, ?, ?)",
                    (survivor_key, new_value, survivor["source"], fts_tags),
                )

                # 删除 merged 的主记录
                conn.execute("DELETE FROM memory_vectors WHERE key = ?", (merged_key,))

                # 重建 closure_table（因为因果链接结构变了）
                self._rebuild_closure_table(conn)

                conn.commit()

                return {
                    "survivor_key": survivor_key,
                    "merged_key": merged_key,
                    "strategy": strategy,
                    "old_confidence": round(old_confidence, 4),
                    "new_confidence": round(new_confidence, 4),
                    "links_transferred": links_transferred,
                    "causal_transferred": causal_transferred,
                    "tags_merged": len(combined_tags),
                }

            except Exception:
                conn.rollback()
                raise

        except Exception as e:
            print(f"[vmem] merge_memories error: {e}")
            return {"error": str(e)}

    # ------------------------------------------------------------------
    # 上下文管理器
    # ------------------------------------------------------------------

    def close(self):
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
        # 关闭连接池中所有连接
        if hasattr(self, "_pool") and self._pool is not None:
            self._pool.close_all()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# ---------------------------------------------------------------------------
# 便捷函数：供 MCP server 调用
# ---------------------------------------------------------------------------

def search_fusion(
    store: MemoryVectorStore,
    encoder: EmbeddingEngine,
    query: str,
    top_k: int = 10,
    source_filter: Optional[str] = None,
    level_filter: Optional[str] = None,
    tags_filter: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    融合搜索的便捷包装函数。
    自动用 encoder 编码 query，调用 store.search_fusion()，
    再根据 source/level/tags 过滤。
    注意：level_filter 参数名保持不变（向后兼容），过滤 importance 字段。
    """
    query_emb = encoder.encode([query])[0]
    results = store.search_fusion(query=query, query_emb=query_emb, top_k=top_k * 3)

    # 后置过滤
    filtered = []
    for r in results:
        if source_filter and r.get("source", "") != source_filter:
            continue
        if level_filter and r.get("importance", "") != level_filter:
            continue
        if tags_filter:
            entry_tags = r.get("tags", "")
            # Tags are now JSON arrays (D-07), with fallback for legacy comma-separated
            if isinstance(entry_tags, str):
                try:
                    entry_tags = json.loads(entry_tags)
                except (json.JSONDecodeError, TypeError):
                    entry_tags = [t.strip() for t in entry_tags.split(",") if t.strip()]
            entry_tags_set = set(entry_tags) if isinstance(entry_tags, list) else set()
            if not any(t in entry_tags_set for t in tags_filter):
                continue
        filtered.append(r)
        if len(filtered) >= top_k:
            break

    return filtered
