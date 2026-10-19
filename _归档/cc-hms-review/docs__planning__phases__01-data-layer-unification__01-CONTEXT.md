# Phase 1: Data Layer Unification - Context

**Gathered:** 2026-06-17
**Status:** Ready for planning

<domain>
## Phase Boundary

统一两个数据库（vmem.db + evolution_memory.db）为单个 vmem.db，添加 Phase 2-8 所需的全部新表（user_profiles, profile_attributes, causal_links, closure_table, memory_links, topics, session_topics, decay_state），重命名/清理 memory_vectors 列，建立 schema 迁移机制，确保现有 25+ 条记忆无损迁移到新 schema。

</domain>

<decisions>
## Implementation Decisions

### Merge Strategy
- **D-01:** 直接在 vmem.db 上扩展（ADD TABLE / ADD COLUMN），不新建数据库。现有 25 条记忆原地保留。
- **D-02:** evolution_memory.db（仅 2 条测试数据）迁移后直接删除，不做备份。
- **D-03:** 迁移后自动验证：跑 vmem_stats 确认 25 条仍在，抽样 3 条 vmem_search 验证搜索正常。

### Column Cleanup (memory_vectors)
- **D-04:** `related`（JSON 数组）保留不动，Phase 4 新增 memory_links 表后代码逐步迁移，最后再删旧字段。
- **D-05:** `access_count` 删除。Phase 6 FSRS decay_state 从零重新计数。
- **D-06:** `level` 重命名为 `importance`。与 Phase 5 的 confidence（系统评估的可靠度）语义区分——importance 是用户标注的重要性。
- **D-07:** `tags` 从逗号分隔字符串改为 JSON 数组。SQLite 原生支持 JSON 函数查询。

### Migration Strategy
- **D-08:** 新建 `schema_migrations` 表追踪迁移版本（migration_name, applied_at）。
- **D-09:** MCP server 启动时自动检查并执行待执行的迁移（vmem-server.py → get_store() → run_migrations()）。
- **D-10:** 迁移代码集中在 `vmem/migrations.py`，store.py 的初始化调用 `run_migrations()`。
- **D-11:** 不支持 down 迁移/回滚。出错时从备份恢复 vmem.db 文件。

### Indexing
- **D-12:** 所有外键列建单列索引：profile_id, from_id, to_id, ancestor, descendant, memory_key, session_id, topic_id。
- **D-13:** 关键路径建复合索引：causal_links(from_id, relation), memory_links(from_id, link_type)。
- **D-14:** FTS5 扩展到 profile_attributes.attr_value 和 causal_links（字段待定），支持画像属性和因果链的全文搜索。
- **D-15:** topics.centroid 向量查询用全表扫描比较余弦相似度（topic 数预计 < 100，无需 ANN 索引）。

### Claude's Discretion
- 新表的列名和类型按 REQUIREMENTS.md 定义实现，细节由 planner 决定。
- FTS5 trigram tokenizer 延续现有配置。
- WAL 模式和 busy_timeout 延续现有配置。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Definition
- `.planning/PROJECT.md` — 项目总览、Gap Analysis、Tech Stack、Key Decisions
- `.planning/REQUIREMENTS.md` §DATA — DATA-01 ~ DATA-10 完整需求定义
- `.planning/ROADMAP.md` §Phase 1 — Goal, Success Criteria, Requirements traceability

### Current Implementation
- `.claude/mcp-servers/vem/store.py` — MemoryVectorStore 当前实现（表结构、搜索逻辑、FTS5 配置）
- `.claude/mcp-servers/vem-server.py` — MCP server 入口（vmem_store / vmem_search / vmem_recall_lessons / vmem_stats）
- `.claude/memory/memory_manager.py` — evolution_memory.db 的旧实现（将被删除）
- `.claude/memory/vem.db` — 当前数据库（25 条记忆，memory_vectors + memory_fts）
- `.claude/memory/evolution_memory.db` — 待合并的旧数据库（2 条测试数据）

### Hooks (不改，但需了解)
- `.claude/hooks/hermes-error-hook.py` — 错误捕获 hook
- `.claude/hooks/hermes-preference-hook.py` — 偏好提取 hook
- `.claude/hooks/hermes-review-hook.py` — 会话复盘 hook

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `vmem/store.py:MemoryVectorStore` — 核心存储类，_init_db() 是迁移入口点，_get_conn() 返回 WAL 模式连接
- `vmem/store.py:EmbeddingEngine` — bge-small-zh-v1.5 嵌入引擎，512 维归一化向量，无需改动
- `vmem/store.py:search_fusion()` — 融合搜索便捷函数（0.60*向量 + 0.25*全文 + 0.15*时间衰减），Phase 5/6 会修改权重

### Established Patterns
- SQLite WAL 模式 + busy_timeout=5000 — 所有新表沿用
- FTS5 trigram tokenizer — 新增 FTS 表沿用此 tokenizer
- embedding BLOB = float32[512].tobytes() — topics.centroid 沿用此格式
- created_at/updated_at = INTEGER unix timestamp — 新表沿用

### Integration Points
- `vmem-server.py:get_store()` — 延迟初始化入口，迁移在此触发
- `vmem-server.py:get_encoder()` — 嵌入引擎单例，新表的向量操作复用
- `memory_vectors.key` — 所有新表的外键引用此列（如 causal_links.from_id/to_id, decay_state.memory_key）

</code_context>

<specifics>
## Specific Ideas

- level → importance 重命名体现了用户对"用户标注"vs"系统评估"的语义区分意识
- tags 改 JSON 数组是用户主动选择，偏好结构化数据
- 用户倾向"推荐选项"（几乎全部选了 Recommended），说明信任默认最佳实践

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 1-Data Layer Unification*
*Context gathered: 2026-06-17*
