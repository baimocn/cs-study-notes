# 🧠 Hermes Memory System

**让 Claude Code 拥有真正的长期记忆 — 从错误中学习，理解用户偏好，建立知识图谱**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-117%20passed-brightgreen.svg)](tests/)

---

## ✨ 特性

| 能力 | 说明 |
|------|------|
| 🗄️ **统一数据层** | 单 SQLite 文件，13 张表，512 维向量索引 |
| 👤 **用户画像** | 6 维度自动提取（身份/技能/偏好/工具/效率/项目） |
| 🔗 **因果链** | 问题→原因→解法→预防，支持多跳递归查询 |
| 🕸️ **关系图** | 5 种链接类型 + 自动矛盾检测 |
| 📊 **置信度** | 贝叶斯更新，按来源初始化，加权搜索排序 |
| 📉 **FSRS 衰减** | Anki 同款遗忘曲线，越用越强，不用淡化 |
| 🏷️ **话题聚类** | 自动匹配/创建话题，定期重算质心 |
| 🔍 **自省** | 自动 GC 低质量记忆 + 系统健康报告 |

## 🚀 快速开始

### 前置条件

```bash
# Python 3.10+
pip install sentence-transformers numpy mcp
```

### 安装

```bash
# 克隆仓库
git clone https://github.com/baimocn/cc-hms.git
cd cc-hms

# 下载向量模型（~90MB）
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5').save('$HOME/bge-small-zh-v1.5')"

# 一键安装到 ~/.claude/
python install.py

# 重启 Claude Code 即可生效
```

### 验证

在 Claude Code 中输入：
```
vmem_stats
```

---

## 📦 架构

```
cc-hms/
├── vmem/                       # 核心库
│   ├── config.py               # 路径自动检测（支持 config.json 覆盖）
│   ├── store.py                # 25+ 存储方法（MemoryVectorStore）
│   ├── migrations.py           # 13 个 schema 迁移
│   └── backfill.py             # 向量回填工具
├── server/
│   └── vmem-server.py          # MCP Server（12 个工具）
├── hooks/
│   ├── hermes-error-hook.py    # PostToolUse → 错误自动捕获→因果链
│   ├── hermes-preference-hook.py # UserPromptSubmit → 偏好自动提取→画像
│   ├── hermes-profile-session-hook.py # SessionStart → 注入用户画像
│   ├── hermes-introspect-hook.py # SessionEnd → 自省+GC+健康报告
│   ├── hermes-review-hook.py   # SessionEnd → 会话复盘
│   └── _helper.py              # 路径 helper（hooks 共用）
├── tests/                      # 117 个测试用例
├── install.py                  # 一键安装脚本
└── README.md
```

## 🔧 MCP 工具

| 工具 | 功能 | 示例 |
|------|------|------|
| `vmem_store` | 存储记忆 | `vmem_store("key1", "用 Python 写脚本")` |
| `vmem_search` | 语义搜索 | `vmem_search("Python 脚本")` |
| `vmem_recall_lessons` | 检索教训 | `vmem_recall_lessons("编码错误")` |
| `vmem_stats` | 统计信息 | 查看记忆总数、来源分布 |
| `vmem_profile_get` | 查询画像 | `vmem_profile_get(category="tools")` |
| `vmem_profile_set` | 设置画像 | `vmem_profile_set("lang", "python", "identity")` |
| `vmem_causal_chain` | 因果链 | `vmem_causal_chain("err:problem:abc123")` |
| `vmem_causal_add` | 添加因果 | `vmem_causal_add("A", "B", "caused_by")` |
| `vmem_related` | 关联记忆 | 查询与某记忆关联的所有条目 |
| `vmem_link_add` | 创建链接 | `vmem_link_add("A", "B", "contradicts")` |
| `vmem_topics` | 话题列表 | 查看所有话题聚类 |
| `vmem_introspect` | 健康报告 | 系统自检（GC 候选、矛盾数等） |

## 🪝 Hooks 自动化

```
用户输入  ──→ hermes-recall-hook.py       ──→ 自动搜索相关记忆注入上下文 ⭐新
用户输入  ──→ hermes-preference-hook.py    ──→ 自动提取偏好到画像
工具失败  ──→ hermes-error-hook.py         ──→ 自动创建因果链
会话开始  ──→ hermes-profile-session-hook  ──→ 注入画像+近期记忆+教训 ⭐增强
会话结束  ──→ hermes-introspect-hook.py    ──→ 自省 GC + 健康报告
会话结束  ──→ hermes-review-hook.py        ──→ 会话复盘提取教训
```

> **关键改进**：`hermes-recall-hook` 让记忆系统从"只写不读"变成"读写平衡"——
> 每条用户消息都会自动触发语义搜索，将相关历史记忆注入 Claude 的上下文。

## 🧮 搜索算法

融合 4 个维度的加权搜索：

```
最终得分 = 0.50 × 向量相似度
         + 0.20 × 全文匹配（FTS5 trigram）
         + 0.20 × 置信度（贝叶斯更新）
         + 0.10 × FSRS 可检索性（自适应衰减）
```

### FSRS 遗忘曲线

```
R(t) = (1 + t / (9 × S))^(-1)
```

| 记忆类型 | 基础稳定性 |
|---------|-----------|
| 错误/教训 | 90 天 |
| 用户偏好 | 180 天 |
| 会话记忆 | 7 天 |
| 默认 | 30 天 |

每次成功召回：**稳定性 += 10%**（可复利叠加）

## ⚙️ 配置

### 自动检测（默认）

所有路径基于 `Path.home()` 自动适配，无需手动配置。

### 手动覆盖

**方式 1：config.json**

创建 `~/.claude/memory/config.json`：

```json
{
  "db_path": "D:/custom/path/vmem.db",
  "model_path": "D:/models/bge-small-zh-v1.5"
}
```

**方式 2：环境变量**

```bash
# Windows
set HMS_DB_PATH=D:\custom\vmem.db
set HMS_MODEL_PATH=D:\models\bge-small-zh-v1.5

# Linux/Mac
export HMS_DB_PATH=/custom/vmem.db
export HMS_MODEL_PATH=/models/bge-small-zh-v1.5
```

## 🧪 测试

```bash
# 运行全部测试（需要已有 vmem.db）
python -m pytest tests/ -v

# 仅运行新功能测试
python -m pytest tests/test_profile_store.py tests/test_causal_store.py tests/test_memory_links.py tests/test_confidence.py tests/test_decay.py tests/test_topics.py tests/test_introspect.py -v
```

## 🗑️ 卸载

```bash
python install.py --uninstall
```

## 📄 数据库 Schema

| 表 | 用途 | Phase |
|----|------|-------|
| `memory_vectors` | 核心记忆存储（含向量、置信度） | 1, 5 |
| `memory_fts` | FTS5 全文索引 | 1 |
| `user_profiles` | 用户画像层级 | 2 |
| `profile_attributes` | 画像属性（6 维度） | 2 |
| `profile_attr_fts` | 画像 FTS5 索引 | 2 |
| `causal_links` | 因果关系链接 | 3 |
| `causal_links_fts` | 因果链 FTS5 索引 | 3 |
| `closure_table` | 因果链多跳查询 | 3 |
| `memory_links` | 记忆关系图 | 4 |
| `confidence_log` | 置信度变化日志 | 5 |
| `decay_state` | FSRS 衰减状态 | 6 |
| `topics` | 话题聚类 | 7 |
| `session_topics` | 记忆-话题关联 | 7 |

## 📜 License

MIT

---

> **Hermes** — 希腊神话中的信使之神，掌管信息传递与智慧。
>
> 8 phases · 117 tests · 25+ methods · 12 MCP tools · 5 hooks · 13 tables
