# Hermes Memory System Upgrade

## What This Is
升级现有 vmem 向量记忆系统，从被动存储进化为 Hermes 级智能记忆——能主动捕获错误、理解用户画像、建立因果链、跨会话关联。

## Core Value
让 Claude Code 真正"认识"用户并从错误中学习，而不是每次会话都从零开始。

## Current State
- vmem.db: SQLite + FTS5 + 512维 bge-small-zh-v1.5 向量（25+ 条记忆）
- 三个 Hermes hook 已运行（error/preference/review）
- MCP server: vmem_store / vmem_search / vmem_recall_lessons / vmem_stats
- 搜索: 融合 0.60*向量 + 0.25*全文 + 0.15*时间衰减

## Gap Analysis
| 能力 | 当前状态 | 目标 |
|------|---------|------|
| 用户画像 | 零散偏好条目 | 结构化分层模型 |
| 因果链 | "是什么" 教训 | "为什么+怎么防+关联" |
| 置信度 | 无评估 | 低→待验证，高→自动应用 |
| 衰减遗忘 | access_count 未使用 | 越用越强，不用淡化 |
| 跨会话关联 | 记忆独立 | 关系图谱 |
| 自省能力 | 无 | 定期评估记忆质量 |

## Tech Stack
- Python 3.14 + SQLite + NumPy
- bge-small-zh-v1.5 (512维, sentence-transformers)
- FTS5 trigram tokenizer
- Claude Code hooks (PreToolUse / PostToolUse / UserPromptSubmit / SessionEnd)
- Claude Code MCP server

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 复用 vmem.db 而非新建 | 减少依赖，统一搜索 | — Pending |
| hook 直接调 Python API | hooks 无法调 MCP | — Pending |
| 置信度用 LLM 评估 | 短文本语义判断需 LLM | — Pending |
| 衰减用时间+访问频率 | 简单有效 | — Pending |

## Requirements

### Validated
- ✓ 向量语义搜索（vmem_search）
- ✓ FTS5 全文搜索
- ✓ 工具失败自动捕获（hermes-error-hook）
- ✓ 用户偏好自动提取（hermes-preference-hook）
- ✓ 会话结束复盘（hermes-review-hook）

### Active
- [ ] 结构化用户画像系统
- [ ] 因果链记忆（问题→原因→解法→预防→关联）
- [ ] 记忆置信度评估
- [ ] 记忆衰减与强化机制
- [ ] 跨会话记忆关联
- [ ] 自省评估能力

### Out of Scope
- 实时边聊边学 — 延迟太高，用 hook 事后处理
- 多用户支持 — 单用户系统
- 可视化 UI — 纯 CLI

## Evolution
This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-06-17 after initialization*
