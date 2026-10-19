"""
vmem MCP Server - 向量记忆服务
使用 FastMCP (mcp Python SDK) 提供向量存储和检索能力。
通过 stdio 方式被 Claude Code 调用。

路径自动检测 — 基于当前用户主目录，无需修改。
"""

import sys
import os
import json
from pathlib import Path

# 确保 vmem 包可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from vmem.config import DB_PATH, MODEL_PATH

# 延迟导入
_store_instance = None
_encoder_instance = None


def get_encoder():
    global _encoder_instance
    if _encoder_instance is None:
        from vmem.store import EmbeddingEngine
        _encoder_instance = EmbeddingEngine(model_path=MODEL_PATH)
    return _encoder_instance


def get_store():
    global _store_instance
    if _store_instance is None:
        from vmem.store import MemoryVectorStore
        encoder = get_encoder()
        _store_instance = MemoryVectorStore(db_path=DB_PATH, embedding_engine=encoder)
    return _store_instance


mcp = FastMCP(
    "vmem",
    description="Hermes Memory System — 向量记忆、用户画像、因果链、关系图、置信度、衰减、话题聚类、自省",
)


@mcp.tool()
def vmem_store(
    key: str,
    value: str,
    source: str = "user",
    level: str = "normal",
    tags: list[str] | None = None,
    related: list[str] | None = None,
) -> str:
    """存储一条记忆到向量数据库。"""
    store = get_store()
    encoder = get_encoder()
    embedding = encoder.encode(value)
    dim = len(embedding) if embedding is not None else 0
    tags_str = json.dumps(tags, ensure_ascii=False) if tags else "[]"
    store.store(key=key, value=value, source=source, level=level, tags=tags_str, related=related or [], embedding=embedding)
    return json.dumps({"ok": True, "key": key, "dim": dim}, ensure_ascii=False)


@mcp.tool()
def vmem_search(
    query: str,
    top_k: int = 10,
    source_filter: str | None = None,
    level_filter: str | None = None,
    tags_filter: list[str] | None = None,
    topic_filter: int | None = None,
) -> str:
    """语义搜索记忆条目（融合向量+全文+时间衰减+置信度）。"""
    from vmem.store import search_fusion
    store = get_store()
    encoder = get_encoder()
    results = search_fusion(store=store, encoder=encoder, query=query, top_k=top_k,
                            source_filter=source_filter, level_filter=level_filter,
                            tags_filter=tags_filter)
    formatted = [{"key": r.get("key",""), "value": r.get("value",""), "source": r.get("source",""),
                  "importance": r.get("importance",""), "tags": r.get("tags",[]),
                  "score": round(r.get("score",0),4), "updated_at": r.get("updated_at","")} for r in results]
    return json.dumps(formatted, ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_recall_lessons(query: str = "", top_k: int = 5) -> str:
    """检索教训和经验。"""
    from vmem.store import search_fusion
    store = get_store()
    encoder = get_encoder()
    effective_query = query if query.strip() else "教训 经验 注意事项"
    results = search_fusion(store=store, encoder=encoder, query=effective_query, top_k=top_k*3)
    lesson_results = []
    for r in results:
        is_lesson = r.get("source","") == "lesson"
        if not is_lesson:
            tags_str = r.get("tags","")
            tags_set = set(t.strip() for t in tags_str.split(",") if t.strip()) if isinstance(tags_str, str) else set(tags_str)
            is_lesson = "lesson" in tags_set
        if is_lesson:
            lesson_results.append(r)
        if len(lesson_results) >= top_k:
            break
    if not lesson_results:
        return "未找到相关教训记录。"
    lines = ["## 教训与经验检索结果\n"]
    for i, r in enumerate(lesson_results, 1):
        lines.append(f"### {i}. [{r.get('key','')}] (相关度: {round(r.get('score',0),4)})")
        lines.append(f"- **标签:** {r.get('tags','')}")
        lines.append(f"- **内容:** {r.get('value','')}\n")
    return "\n".join(lines)


@mcp.tool()
def vmem_stats() -> str:
    """返回向量记忆数据库的统计信息。"""
    return json.dumps(get_store().get_stats(), ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_profile_get(key: str = "", category: str = "") -> str:
    """查询用户画像属性。"""
    results = get_store().profile_get(attr_key=key if key else None, category=category if category else None)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_profile_set(key: str, value: str, category: str = "preferences", confidence: float = 0.5) -> str:
    """设置用户画像属性。"""
    ok = get_store().profile_set(attr_key=key, attr_value=value, category=category, confidence=confidence, source="user-explicit")
    return json.dumps({"ok": ok, "key": key, "category": category})


@mcp.tool()
def vmem_causal_chain(key: str, max_depth: int = 5) -> str:
    """查询记忆的因果链。"""
    return json.dumps(get_store().causal_chain(key, max_depth), ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_causal_add(from_key: str, to_key: str, relation: str, strength: float = 1.0) -> str:
    """添加因果关系链接。"""
    ok = get_store().causal_add(from_key, to_key, relation, strength)
    return json.dumps({"ok": ok, "from": from_key, "to": to_key, "relation": relation})


@mcp.tool()
def vmem_causal_get(key: str) -> str:
    """获取记忆的直接因果链接。"""
    return json.dumps(get_store().causal_get(key), ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_related(key: str, link_type: str = "") -> str:
    """查询记忆的关联记忆。"""
    store = get_store()
    links = store.link_get(key, link_type if link_type else None)
    enriched = []
    for link in links:
        other_key = link["to_id"] if link["from_id"] == key else link["from_id"]
        other_mem = store.get(other_key)
        enriched.append({**link, "other_key": other_key, "other_value": other_mem["value"] if other_mem else ""})
    return json.dumps(enriched, ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_link_add(from_key: str, to_key: str, link_type: str, strength: float = 1.0) -> str:
    """添加记忆之间的关系链接。"""
    ok = get_store().link_add(from_key, to_key, link_type, strength)
    return json.dumps({"ok": ok, "from": from_key, "to": to_key, "link_type": link_type})


@mcp.tool()
def vmem_topics() -> str:
    """列出所有话题聚类。"""
    return json.dumps(get_store().topic_list(), ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_introspect() -> str:
    """返回记忆系统健康报告。"""
    return json.dumps(get_store().introspect_health(), ensure_ascii=False, indent=2)


@mcp.tool()
def vmem_find_duplicates(threshold: float = 0.92) -> str:
    """基于向量余弦相似度查找重复记忆对。

    扫描所有记忆的 embedding，计算两两相似度，返回高于阈值的重复对。
    当记录数超过 10000 时自动启用分块计算以控制内存。

    Args:
        threshold: 相似度阈值（0-1），默认 0.92，越高越严格。

    Returns:
        JSON 字符串，包含重复对列表（按相似度降序）。
    """
    try:
        results = get_store().find_duplicates(threshold=threshold)
        return json.dumps({
            "ok": True,
            "count": len(results),
            "pairs": results,
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def vmem_merge(key_a: str, key_b: str, strategy: str = "keep_richer") -> str:
    """合并两条记忆为一条，保留幸存者并删除另一条。

    支持三种合并策略：
    - keep_richer: 保留信息更丰富的那条（value 长度、tags 数量、链接数综合评估）
    - keep_newer: 保留 updated_at 较新的那条
    - manual: 以 key_a 为幸存者，合并 key_b 的部分信息

    合并后幸存者的置信度提升 10%（上限 1.0），原有的因果链接和记忆链接会被转移。

    Args:
        key_a: 第一条记忆的 key。
        key_b: 第二条记忆的 key。
        strategy: 合并策略，可选 "keep_richer"、"keep_newer"、"manual"。

    Returns:
        JSON 字符串，包含合并结果（幸存者 key、被合并 key、置信度变化、转移的链接数等）。
    """
    try:
        result = get_store().merge_memories(key_a, key_b, strategy=strategy)
        return json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def vmem_snapshot_export(path: str) -> str:
    """导出当前记忆数据库的完整快照为 JSON 文件。

    包含所有 memory_vectors 记录（向量以 base64 编码）、causal_links、
    memory_links、topics、session_topics 等关联表数据，以及导出元信息。

    Args:
        path: 导出文件的保存路径（绝对路径或相对于工作目录）。

    Returns:
        JSON 字符串，包含导出统计信息（记录数、文件路径、schema 版本等）。
    """
    try:
        result = get_store().snapshot_export(path)
        return json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
def vmem_snapshot_import(path: str, mode: str = "merge") -> str:
    """从 JSON 快照文件导入记忆数据。

    支持三种导入模式：
    - merge: 已有 key 跳过，只导入新记录（默认）
    - overwrite: 清空当前数据后全量导入
    - upsert: 对比 updated_at，保留较新的记录

    导入后会自动重建 FTS5 全文索引并运行 schema 迁移以确保兼容。

    Args:
        path: 快照 JSON 文件路径。
        mode: 导入模式，可选 "merge"、"overwrite"、"upsert"。

    Returns:
        JSON 字符串，包含导入统计信息（导入数、跳过数、覆盖数等）。
    """
    try:
        result = get_store().snapshot_import(path, mode=mode)
        return json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
