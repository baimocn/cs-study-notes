# Roadmap — Hermes Memory System

## Phase 1: Data Layer Unification

**Goal:** 统一数据库，添加所有新表，向后兼容迁移
**Mode:** mvp
**Requirements:** DATA-01 ~ DATA-10
**Plans:** 3/3 plans complete
**Success Criteria**:

1. 单个 vmem.db 包含 12 张表
2. 现有 25+ 条记忆无损迁移到新 schema
3. vmem_search / vmem_store 功能不受影响
4. 所有新表有正确的索引和 WAL 模式

Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Migration framework + 8 new table DDL (Wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02-PLAN.md — Column cleanup + code updates (Wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-03-PLAN.md — Evolution merge + backward compat tests (Wave 3)

## Phase 2: User Profile System

**Goal:** 结构化用户画像，替代零散偏好条目
**Mode:** mvp
**Requirements:** PROF-01 ~ PROF-06
**Plans:** 2 plans
**Success Criteria**:

1. hermes-preference-hook 写入画像表而非 memory_vectors
2. 6 个维度的画像属性可查询
3. SessionStart 自动注入画像摘要
4. 画像属性带置信度和来源

Plans:
**Wave 1**

- [x] 02-01-PLAN.md — Profile store methods + tests (Wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-02-PLAN.md — MCP tools + preference hook rewrite + SessionStart hook (Wave 2)

## Phase 3: Causal Chain Memory

**Goal:** 教训从"是什么"升级到"为什么+怎么防"
**Mode:** mvp
**Requirements:** CAUS-01 ~ CAUS-06
**Success Criteria**:

1. hermes-error-hook 自动创建因果链
2. 因果链可通过 MCP 工具查询
3. closure_table 支持多跳祖先查询
4. 5 种因果关系类型可用

Plans:
**Wave 1**

- [x] 03-01-PLAN.md — Causal chain store methods + closure_table + tests (Wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02-PLAN.md — MCP tools + error hook rewrite (Wave 2)

## Phase 4: Memory Relation Graph

**Goal:** 记忆之间建立类型化关系，替代 related JSON
**Mode:** mvp
**Requirements:** GRAF-01 ~ GRAF-05
**Success Criteria**:

1. memory_links 表替代 related JSON 字段
2. 矛盾检测：新记忆入库时自动扫描
3. supersedes 链自动建立
4. vmem_related 返回关联记忆

Plans:
**Wave 1**

- [x] 04-01-PLAN.md — Memory link methods + contradiction detection (Wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02-PLAN.md — MCP tools (Wave 2)

## Phase 5: Confidence Scoring

**Goal:** 记忆有可信度，避免错误记忆自动应用
**Mode:** mvp
**Requirements:** CONF-01 ~ CONF-05
**Success Criteria**:

1. 写入时自动计算初始置信度
2. 贝叶斯更新在佐证/矛盾/访问时触发
3. 搜索结果按置信度加权
4. 置信度变化有日志可追溯

Plans:
**Wave 1**

- [x] 05-01-PLAN.md — Confidence scoring (migrations, methods, search fusion) (Wave 1)

## Phase 6: FSRS Memory Decay

**Goal:** Anki 同款遗忘曲线，越用越强不用淡化
**Mode:** mvp
**Requirements:** DECA-01 ~ DECA-05
**Success Criteria**:

1. FSRS-4.5 替代固定 7 天半衰期
2. 按记忆类型分基础半衰期
3. 访问强化正确计算
4. 衰减只影响排名不删除数据

Plans:
**Wave 1**

- [x] 06-01-PLAN.md — FSRS decay (methods, search integration) (Wave 1)

## Phase 7: Cross-Session Topic Clustering

**Goal:** 自动关联相关会话的记忆
**Mode:** mvp
**Requirements:** CLUS-01 ~ CLUS-05
**Success Criteria**:

1. 新记忆自动匹配 topic centroid
2. topic centroid 定期重算
3. vmem_search 支持 topic_filter
4. SessionEnd 生成会话摘要

Plans:
**Wave 1**

- [x] 07-01-PLAN.md — Topic clustering (methods, search filter, MCP tool) (Wave 1)

## Phase 8: Self-Reflection & Introspection

**Goal:** 系统能自我评估和优化
**Mode:** mvp
**Requirements:** INTR-01 ~ INTR-05
**Success Criteria**:

1. 低置信度记忆自动标记归档
2. 矛盾检测定期扫描
3. 从 episodic memories 提取新画像属性
4. vmem_introspect 返回健康报告

Plans:
**Wave 1**

- [x] 08-01-PLAN.md — Introspection (GC, health, hook) (Wave 1)

## Traceability

| Phase | Requirements |
|-------|-------------|
| 1 | DATA-01~10 |
| 2 | PROF-01~06 |
| 3 | CAUS-01~06 |
| 4 | GRAF-01~05 |
| 5 | CONF-01~05 |
| 6 | DECA-01~05 |
| 7 | CLUS-01~05 |
| 8 | INTR-01~05 |
