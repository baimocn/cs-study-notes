#!/usr/bin/env python3
"""
Hermes Review Hook - 会话结束时自动分析 transcript，提取教训和决策

从 stdin 读取 JSON:
  { "session_id": "...", "transcript_path": "..." }

分析最后 100 条消息，提取：
  - 重复错误（同一工具对同一文件失败 > 1 次）-> permanent 教训
  - 修正决策（assistant 说"不对"/"错了"后给新方案）
  - 用户反馈（user 说"没生效"/"不对"等）
  - 成功模式（操作序列最终成功）

使用 HookWriter 进行多进程安全写入。
"""

import json
import os
import re
import signal
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# 确保 hook 模块可导入
_HOOKS_DIR = Path(__file__).parent
if str(_HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOKS_DIR))

# ---------------------------------------------------------------------------
# 超时保护：15 秒
# ---------------------------------------------------------------------------

class _Timeout(Exception):
    pass


def _alarm_handler(signum, frame):
    raise _Timeout("hermes-review-hook timed out")


def _setup_timeout(seconds: int):
    """设置超时。SIGALRM 用于 Unix，threading timer 用于 Windows 兜底。"""
    try:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(seconds)
    except (AttributeError, OSError):
        # Windows 没有 SIGALRM，用 threading 兜底
        import threading

        def _raise_timeout():
            # 设置一个标志，让主循环定期检查
            _setup_timeout._timed_out = True

        _setup_timeout._timed_out = False
        timer = threading.Timer(seconds, _raise_timeout)
        timer.daemon = True
        timer.start()

# ---------------------------------------------------------------------------
# DB path
# ---------------------------------------------------------------------------

def _get_db_path() -> str:
    env = os.environ.get("HMS_DB_PATH")
    if env:
        return env
    return str(Path.home() / ".claude" / "memory" / "vmem.db")

# ---------------------------------------------------------------------------
# 延迟加载 vmem store（通过 HookWriter）
# ---------------------------------------------------------------------------

_hook_writer = None


def _get_writer():
    """懒加载 HookWriter。"""
    global _hook_writer
    if _hook_writer is None:
        from _hook_writer import HookWriter
        _hook_writer = HookWriter(_get_db_path(), timeout_sec=3.0)
    return _hook_writer


# ---------------------------------------------------------------------------
# Transcript 解析
# ---------------------------------------------------------------------------

def _read_last_messages(transcript_path: str, max_lines: int = 100) -> list:
    """读取 JSONL transcript 的最后 max_lines 行，返回解析后的消息列表。"""
    path = Path(transcript_path)
    if not path.exists() or path.stat().st_size == 0:
        return []

    # 用双端队列只保留最后 max_lines 行，避免大文件 OOM
    from collections import deque
    tail = deque(maxlen=max_lines)

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    tail.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except (OSError, IOError):
        return []

    return list(tail)


def _extract_text(msg: dict) -> str:
    """从消息中提取纯文本内容。"""
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
        return " ".join(parts)
    return ""


# ---------------------------------------------------------------------------
# 模式提取
# ---------------------------------------------------------------------------

# 用于匹配工具调用的 key: (tool_name, file_path)
_RE_TOOL_FAIL = re.compile(
    r"(?:Error|Failed|error|failed|Permission denied|No such file|not found)",
    re.IGNORECASE,
)

_RE_ASSISTANT_CORRECTION = re.compile(
    r"(?:不对|错了|让我重新|重新来|我搞错了|搞反了|纠正|更正|"
    r"actually|let me redo|my mistake|I was wrong|"
    r"let me correct|correction|wait,|hmm,)",
    re.IGNORECASE,
)

_RE_USER_NEGATIVE = re.compile(
    r"(?:没生效|不对|没通过|还是没|没用|不行|错了|失败|"
    r"doesn.?t work|not working|still (?:not|broken)|failed|wrong|"
    r"没反应|没效果|报错|还是报|又报)",
    re.IGNORECASE,
)


def _parse_tool_calls(messages: list) -> list:
    """从消息列表中提取工具调用信息，返回 [(tool_name, input_params, output_text, success)]。"""
    calls = []
    for msg in messages:
        role = msg.get("role", "")
        if role != "assistant":
            continue

        # 检查 tool_use blocks
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_name = block.get("name", "")
                    tool_input = block.get("input", {})
                    # 输入中可能有文件路径
                    file_path = tool_input.get("file_path", tool_input.get("path", ""))
                    calls.append({
                        "tool": tool_name,
                        "file": str(file_path),
                        "input": tool_input,
                    })
    return calls


def _parse_tool_results(messages: list) -> list:
    """提取工具结果，返回 [(tool_use_id, is_error, text)]。"""
    results = []
    for msg in messages:
        role = msg.get("role", "")
        if role != "user":
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    results.append({
                        "tool_use_id": block.get("tool_use_id", ""),
                        "is_error": block.get("is_error", False),
                        "text": _extract_text({"content": block.get("content", "")}),
                    })
    return results


def extract_repeated_errors(messages: list) -> list:
    """提取重复错误：同一工具对同一文件失败 > 1 次。"""
    # 简化：扫描所有 assistant 消息中的工具调用 + error 模式
    # 因为 transcript JSONL 格式可能多样，用文本匹配兜底
    failure_counts = Counter()
    failure_details = {}

    for msg in messages:
        text = _extract_text(msg)
        if not text:
            continue

        # 尝试匹配 "工具名 ... 文件路径 ... error" 的模式
        # 常见模式: Edit failed on /path/to/file
        tool_fail_match = re.findall(
            r"(Edit|Write|Read|Bash|Grep|Glob|Agent)\s.*?"
            r"([A-Za-z]:[/\\][^\s\"']+|/[^\s\"']+)",
            text,
        )
        if _RE_TOOL_FAIL.search(text):
            for tool, filepath in tool_fail_match:
                key = (tool, filepath)
                failure_counts[key] += 1
                failure_details[key] = text[:200]

    results = []
    for (tool, filepath), count in failure_counts.items():
        if count > 1:
            results.append({
                "type": "repeated_error",
                "tool": tool,
                "file": filepath,
                "count": count,
                "detail": failure_details.get((tool, filepath), ""),
            })

    return results


def extract_correction_decisions(messages: list) -> list:
    """提取修正决策：assistant 表示之前的方案有误后给出新方案。"""
    results = []
    for i, msg in enumerate(messages):
        text = _extract_text(msg)
        if not text:
            continue
        if msg.get("role") == "assistant" and _RE_ASSISTANT_CORRECTION.search(text):
            # 取这段文字和后续一句话作为决策描述
            snippet = text[:300].strip()
            results.append({
                "type": "correction_decision",
                "detail": snippet,
                "index": i,
            })
    return results


def extract_user_feedback(messages: list) -> list:
    """提取用户负面反馈。"""
    results = []
    for i, msg in enumerate(messages):
        text = _extract_text(msg)
        if not text:
            continue
        if msg.get("role") == "user" and _RE_USER_NEGATIVE.search(text):
            snippet = text[:200].strip()
            results.append({
                "type": "user_negative_feedback",
                "detail": snippet,
                "index": i,
            })
    return results


def extract_success_patterns(messages: list) -> list:
    """提取成功模式：检测成功标记（如 git commit、测试通过等）。"""
    results = []
    for msg in messages:
        text = _extract_text(msg)
        if not text:
            continue
        if msg.get("role") == "assistant":
            # git commit 成功
            if re.search(r"(?:committed|merge|PR|pull request)", text, re.IGNORECASE):
                snippet = text[:200].strip()
                results.append({
                    "type": "success_pattern",
                    "category": "git",
                    "detail": snippet,
                })
            # 测试通过
            elif re.search(r"(?:all tests? pass|测试通过|passed|build succeeded)", text, re.IGNORECASE):
                snippet = text[:200].strip()
                results.append({
                    "type": "success_pattern",
                    "category": "test",
                    "detail": snippet,
                })

    # 去重：同一类别只保留最后一条
    by_cat = {}
    for r in results:
        by_cat[r["category"]] = r
    return list(by_cat.values())


# ---------------------------------------------------------------------------
# 去重 + 存储
# ---------------------------------------------------------------------------

def _sanitize_fts_query(text: str) -> str:
    """将文本清理为 FTS5 trigram 安全的查询字符串。"""
    # FTS5 MATCH 的 trigram 模式对特殊字符敏感，替换掉非字母数字字符
    cleaned = re.sub(r"[^a-zA-Z0-9一-鿿]+", " ", text)
    cleaned = cleaned.strip()
    # FTS5 MATCH 至少需要 3 个字符（trigram 最小单位）
    if len(cleaned) < 3:
        return ""
    return cleaned


def _is_duplicate(writer, query_text: str, threshold: float = 0.85) -> bool:
    """用 vmem 的 FTS 检查是否已有类似记忆。"""
    try:
        safe_query = _sanitize_fts_query(query_text[:80])
        if not safe_query:
            return False
        results = writer.search_fts(safe_query, top_k=3)
        for r in results:
            if r.get("score", 0) > threshold:
                return True
        return False
    except Exception:
        return False


def _store_lesson(writer, session_prefix: str, lesson: dict) -> None:
    """存储一条教训到 vmem（通过 HookWriter）。"""
    try:
        lesson_type = lesson.get("type", "unknown")
        detail = lesson.get("detail", "")
        is_repeated = lesson_type == "repeated_error"

        # 去重
        dedup_query = f"{lesson_type}: {detail[:60]}"
        if _is_duplicate(writer, dedup_query):
            return

        # 构造 value
        value = json.dumps(lesson, ensure_ascii=False)

        writer.store_memory(
            key=f"review:{session_prefix}:{lesson_type}:{int(time.time())}",
            value=value,
            source="auto-review",
            level="permanent" if is_repeated else "long",
            tags=f"review,{lesson_type},auto",
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 主逻辑
# ---------------------------------------------------------------------------

def _check_timeout(start_time: float, timeout: float) -> bool:
    """检查是否超时（兼容 Windows 的 threading 方案）。"""
    if time.monotonic() - start_time > timeout:
        return True
    if hasattr(_setup_timeout, "_timed_out") and _setup_timeout._timed_out:
        return True
    return False


def main():
    # 设置超时
    _setup_timeout(15)

    start_time = time.monotonic()
    TIMEOUT = 14  # 留 1 秒余量

    try:
        # 1. 从 stdin 读取输入
        raw = sys.stdin.read().strip()
        if not raw:
            return

        try:
            input_data = json.loads(raw)
        except json.JSONDecodeError:
            return

        session_id = input_data.get("session_id", "")
        transcript_path = input_data.get("transcript_path", "")

        if not transcript_path or not Path(transcript_path).exists():
            return

        # 2. 读取最后 100 条消息
        messages = _read_last_messages(transcript_path, max_lines=100)
        if not messages:
            return

        session_prefix = session_id[:8] if session_id else "unknown"

        # 3. 提取各种模式
        lessons = []

        # 3a. 重复错误
        repeated = extract_repeated_errors(messages)
        lessons.extend(repeated)

        # 检查超时
        if _check_timeout(start_time, TIMEOUT):
            return

        # 3b. 修正决策
        corrections = extract_correction_decisions(messages)
        # 限制数量，避免过多
        lessons.extend(corrections[:5])

        if _check_timeout(start_time, TIMEOUT):
            return

        # 3c. 用户负面反馈
        feedback = extract_user_feedback(messages)
        lessons.extend(feedback[:5])

        if _check_timeout(start_time, TIMEOUT):
            return

        # 3d. 成功模式
        successes = extract_success_patterns(messages)
        lessons.extend(successes)

        # 4. 存储（去重后）— 使用 HookWriter 多进程安全写入
        if lessons:
            from _hook_writer import HookWriter
            db_path = _get_db_path()
            with HookWriter(db_path, timeout_sec=3.0) as writer:
                for lesson in lessons:
                    if _check_timeout(start_time, TIMEOUT):
                        break
                    _store_lesson(writer, session_prefix, lesson)

    except _Timeout:
        pass
    except Exception:
        # 静默处理所有异常
        pass
    finally:
        # 确保不输出任何内容到 stdout
        pass


if __name__ == "__main__":
    main()
