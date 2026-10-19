#!/usr/bin/env python3
"""
Hermes Recall Hook — UserPromptSubmit
每次用户发消息时，自动搜索相关记忆并注入上下文。
让 Claude 在回答前就能看到相关历史，而非事后才想起来。

5-second hard timeout.
"""
import sys
import json
import signal


class _Timeout(Exception):
    pass


def _alarm_handler(signum, frame):
    raise _Timeout()


if hasattr(signal, "SIGALRM"):
    signal.signal(signal.SIGALRM, _alarm_handler)


def _build_recall_output(prompt: str, db_path: str) -> dict:
    """Search for related memories and format as hook output."""
    if not prompt or len(prompt) < 5 or len(prompt) > 2000:
        return {}

    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from _helper import get_db_path
    from vmem.store import MemoryVectorStore, EmbeddingEngine, search_fusion

    effective_db = db_path if db_path else get_db_path()
    engine = EmbeddingEngine()
    store = MemoryVectorStore(effective_db, embedding_engine=engine)

    results = search_fusion(
        store=store,
        encoder=engine,
        query=prompt,
        top_k=3,
    )

    store.close()

    if not results:
        return {}

    filtered = [r for r in results if r.get("score", 0) > 0.3]
    if not filtered:
        return {}

    lines = ["## Related Memories (auto-recalled)"]
    for r in filtered:
        key = r.get("key", "")
        value = r.get("value", "")
        source = r.get("source", "")
        score = round(r.get("score", 0), 2)
        preview = value[:200].replace("\n", " ")
        lines.append(f"- [{key}] ({source}, score:{score}) {preview}")

    context = "\n".join(lines)

    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }


def main():
    if hasattr(signal, "SIGALRM"):
        signal.alarm(5)
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        prompt = data.get("prompt", "")

        if not prompt:
            return

        output = _build_recall_output(prompt, "")

        if output:
            print(json.dumps(output, ensure_ascii=False))

    except (_Timeout, Exception):
        pass
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)


if __name__ == "__main__":
    main()
