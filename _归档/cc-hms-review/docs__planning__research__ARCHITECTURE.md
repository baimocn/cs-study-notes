# AI Memory System Architecture Research

## Current System Inventory

### Existing databases (4 SQLite files)
```
~/.claude/memory/
  vmem.db              -- Vector + FTS5 store (MemoryVectorStore)
  memory.db            -- Simple key-value memories (unused / legacy)
  evolution_memory.db  -- MemoryManager with working/short/long/permanent tiers
~/.claude/learning/
  learning.db          -- Learning engine (unused / legacy)
  evolution_learning.db -- LearningEngine with patterns table
```

### Existing MCP servers (3 servers)
```
vmem          -> vmem-server.py   -> MemoryVectorStore (vector + FTS5)
evolution     -> evolution-server.py -> MemoryManager + LearningEngine
memory        -> (mcp__memory__*)  -> Knowledge graph (entities + relations + observations)
```

### Existing hooks
```
memory-hook.py   -- SessionStart/SessionEnd: store session info, cleanup expired
learning-hook.py -- PostToolUse: record tool use as learning entries
```

### Current data flow
```
User conversation
  |
  v
CLAUDE.md instructions -> Claude calls MCP tools
  |
  +-> vmem_store(key, value, source, level, tags)   -> vmem.db  (vector + FTS5)
  +-> memory_store(key, value, level)                -> evolution_memory.db
  +-> learning_record(type, desc, context, outcome)  -> evolution_learning.db
  +-> create_entities / add_observations             -> knowledge graph (in-memory JSON?)
```

### Current fusion scoring (vmem.search_fusion)
```
score = 0.60 * vector_similarity
      + 0.25 * fts5_trigram_rank
      + 0.15 * time_decay(7-day half-life)
```

---

## Reference Architectures (Field Survey)

### 1. Stanford Generative Agents (Park et al., 2023)

The foundational paper for agent memory systems. Three components:

- **Memory Stream**: Append-only log of all observations. Each entry has: (text, timestamp, importance_score, embedding).
- **Retrieval**: At query time, combines three signals:
  - Recency: exponential decay, half-life configurable
  - Importance: LLM-scored 1-10 at write time (stored with the entry)
  - Relevance: cosine similarity of embeddings
  - Final: normalized weighted sum of all three
- **Reflection**: Periodically (when cumulative importance exceeds threshold), the agent synthesizes higher-order insights from recent memories. Reflections are stored back into the memory stream as new entries (with higher importance).

Key insight: importance is scored at write time by the LLM, not at read time.

### 2. MemGPT / Letta (Packer et al., 2023; Letta 2024-25)

Operating-system metaphor for memory management:

- **Main Context** (== working memory): Always in the LLM's context window. Contains:
  - System instructions
  - Core Memory: small key-value block the LLM can self-edit (user name, preferences, current goals)
  - Summary of recent conversation
- **Archival Storage** (== disk): Long-term vector store for anything that falls out of context. The LLM can search it via tools.
- **Recall Storage** (== swap): Past conversation transcripts. Searchable.

Key insight: the LLM itself decides what to page in/out. Self-editing memory means the agent writes its own core memory entries via function calls.

### 3. Mem0 (2024-25)

Open-source memory layer. Architecture:

- **Memory extraction**: After each conversation turn, an LLM call extracts facts that should be persisted (user preferences, decisions, corrections).
- **Memory types**: user_memory, session_memory, agent_memory -- scoped by ID.
- **Deduplication**: Before storing, search existing memories for semantically similar entries. Update in-place rather than duplicate.
- **Graph layer**: Optionally stores relationships between entities as a graph (subject-predicate-object triples).
- **Hybrid search**: Vector similarity + keyword filter + metadata filter.

Key insight: automatic extraction + deduplication at write time is critical for memory quality.

### 4. Cognee / Cognify (2024)

Knowledge-graph-first approach:

- Extract entities and relationships from conversations
- Build a property graph (nodes = entities, edges = relationships with properties)
- Store embeddings on nodes for hybrid graph + vector retrieval
- Query with graph traversal + vector similarity

---

## Design Decisions for Our System

### Decision 1: Single DB vs Multi-DB

**Recommendation: Single consolidated SQLite file.**

Rationale:
- The current 4-file layout (vmem.db, memory.db, evolution_memory.db, evolution_learning.db) creates confusion about which is authoritative.
- SQLite handles multiple tables and WAL concurrency well for single-user desktop.
- One file means one backup, one migration script, one integrity check.
- The knowledge graph (currently separate, JSON-backed) can live in the same file.

Proposed layout:
```
~/.claude/memory/
  vmem.db    -- THE single database (rename to claude_memory.db in future)
    Tables:
    - memories          (core fact/observation store, replaces memory_vectors)
    - memories_fts      (FTS5 index)
    - sessions          (session tracking)
    - causal_links      (DAG edges between memories)
    - user_profile      (key-value profile attributes)
    - learning_entries  (merged from evolution_learning.db)
    - learning_patterns (merged from evolution_learning.db)
    - embeddings        (separate table for embeddings, allows hot-swap of model)
    - memory_tags       (normalized tags, many-to-many)
```

### Decision 2: User Profile Schema

**Recommendation: Key-value with document blobs, NOT a graph.**

Rationale:
- A user profile is fundamentally a set of attribute-value pairs (name, language, preferences, coding style, tech stack).
- Graph adds complexity without benefit for a single user -- there are no cross-user relationships to model.
- Some attributes are simple scalars (language: "zh"), others are structured documents (tech_stack: {languages: [...], frameworks: [...]}).

Schema:
```sql
CREATE TABLE user_profile (
    attr_key    TEXT PRIMARY KEY,       -- e.g. "preferred_language", "coding_style"
    attr_value  TEXT NOT NULL,          -- scalar string or JSON document
    confidence  REAL DEFAULT 0.8,      -- how certain we are about this
    source      TEXT DEFAULT '',        -- where we learned this (conversation_id, explicit, inferred)
    updated_at  INTEGER NOT NULL,
    created_at  INTEGER NOT NULL
);

-- Example rows:
-- preferred_language  | "zh"                    | 0.95 | "explicit"     | ...
-- tech_stack          | {"languages":["python","typescript"],"frameworks":["next.js","fastapi"]} | 0.85 | "inferred" | ...
-- editor              | "VS Code"               | 0.90 | "conversation" | ...
```

Why not a document store? SQLite JSON functions (json_extract, json_each) give us document querying without the overhead of a separate DB. For a single-user system, key-value + JSON blobs is the sweet spot.

### Decision 3: Causal Chains -- DAG in SQLite

**Recommendation: Adjacency list pattern (edge table) with closure table for fast ancestor queries.**

Causal chains represent "A caused B" or "A led to B". These are naturally directed acyclic graphs (DAGs).

Schema:
```sql
-- Direct edges (parent -> child)
CREATE TABLE causal_links (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id     TEXT NOT NULL,        -- memory key (FK to memories.key)
    to_id       TEXT NOT NULL,        -- memory key (FK to memories.key)
    relation    TEXT NOT NULL,        -- "caused", "led_to", "resolved", "contradicts", "supersedes"
    strength    REAL DEFAULT 1.0,    -- how strong the causal link is (0-1)
    created_at  INTEGER NOT NULL,
    UNIQUE(from_id, to_id, relation)
);

-- Closure table for transitive queries ("what caused Z?" across N hops)
CREATE TABLE causal_closure (
    ancestor    TEXT NOT NULL,
    descendant  TEXT NOT NULL,
    depth       INTEGER NOT NULL,     -- 1 = direct, 2 = grandparent, etc.
    relation    TEXT NOT NULL,
    PRIMARY KEY (ancestor, descendant, relation)
);

-- Triggers or application logic must maintain closure table on insert/delete
```

Why closure table instead of recursive CTEs alone?
- Recursive CTEs work in SQLite (since 3.8.3), but they scan the full edge table each time.
- Closure table makes "all ancestors of X" or "all descendants of Y" a single indexed lookup.
- For a desktop system with thousands of memories, the closure table size is manageable.
- Can fall back to recursive CTE for depth > 5 (closure table up to depth 5, CTE beyond).

Alternative considered: Linked list (next/prev pointers). Rejected because memories can have multiple causes and multiple effects -- it is fundamentally a DAG, not a chain.

Example causal chain:
```
"project_x_build_fails" --[caused]--> "discovered_dependency_conflict"
"discovered_dependency_conflict" --[led_to]--> "pinned_package_versions"
"pinned_package_versions" --[resolved]--> "project_x_build_passes"
```

### Decision 4: Confidence Scoring -- Store-Time + Query-Time Adjustment

**Recommendation: Score at store time, adjust at query time.**

Two distinct confidence values:
1. **Epistemic confidence** (store-time): How certain are we this fact is true?
2. **Relevance confidence** (query-time): How relevant is this to the current query?

#### Store-time epistemic confidence:
```
confidence = base_confidence * source_reliability * corroboration_factor

Where:
- base_confidence: LLM's self-assessed confidence (0-1) when it writes the memory
- source_reliability: multiplier based on source type
  - explicit_user_statement: 1.0
  - inferred_from_conversation: 0.8
  - llm_generated_reflection: 0.6
  - auto_extracted: 0.5
- corroboration_factor: 1.0 + 0.1 * (num_corroborating_entries - 1), capped at 1.5
  (multiple sources saying the same thing increases confidence)
```

#### Query-time relevance confidence:
```
relevance = similarity * recency_decay * access_boost * epistemic_confidence

Where:
- similarity: cosine similarity from embedding match (0-1)
- recency_decay: 2^(-elapsed/half_life) -- existing time decay
- access_boost: 1.0 + 0.05 * log(access_count + 1) -- frequent access = more trusted
- epistemic_confidence: the stored confidence value
```

Schema addition to memories table:
```sql
ALTER TABLE memories ADD COLUMN confidence REAL DEFAULT 0.8;
ALTER TABLE memories ADD COLUMN source_type TEXT DEFAULT 'auto';  -- explicit, inferred, reflection, auto
ALTER TABLE memories ADD COLUMN corroborated_by TEXT DEFAULT '[]'; -- JSON list of confirming memory keys
```

### Decision 5: Cross-Session Linking -- Topic Threading

**Recommendation: Topic clusters via embedding clustering + explicit session_topic linking.**

Problem: "Same topic across sessions" is ambiguous. Three concrete scenarios:
1. Continuing a conversation about the same project (easy: project name is explicit)
2. Revisiting a technical decision (medium: embedding similarity catches this)
3. Revisiting a user preference that evolved (hard: need versioning)

Solution: Two-layer approach.

#### Layer 1: Session-topic bridge table
```sql
CREATE TABLE session_topics (
    session_id  TEXT NOT NULL,
    topic_id    TEXT NOT NULL,       -- a topic is a cluster centroid or a named entity
    relevance   REAL DEFAULT 1.0,
    PRIMARY KEY (session_id, topic_id)
);

CREATE TABLE topics (
    topic_id    TEXT PRIMARY KEY,     -- UUID or hash of centroid
    label       TEXT DEFAULT '',      -- human-readable label (LLM-generated)
    centroid    BLOB,                 -- average embedding of all memories in this topic
    created_at  INTEGER NOT NULL,
    updated_at  INTEGER NOT NULL
);
```

#### Layer 2: Automatic topic assignment
On each memory store:
1. Compute embedding similarity to all existing topic centroids.
2. If best match > 0.75 threshold -> assign to that topic.
3. If no match > 0.75 -> create new topic with this memory as seed.
4. Periodically recompute centroids (on a timer or after N new memories).

#### Layer 3: Session summary linking
Each session produces a summary (existing in session_hook). Store session summaries as memories with source="session_summary". Cross-session linking then falls out naturally: search for the session summary that is most similar to the current query.

### Decision 6: Memory Decay

**Recommendation: Exponential decay with access-reinforced half-life, plus explicit "permanent" override.**

```
effective_weight = base_weight * recency_factor * access_factor

recency_factor = 2^(-age_seconds / half_life_seconds)

half_life_seconds = base_half_life / (1 + access_count * reinforcement_factor)

Where:
- base_half_life = 7 days (168 hours) for normal memories
- base_half_life = 30 days for "important" level
- base_half_life = 365 days for "permanent" level (or infinity)
- reinforcement_factor = 0.1 (each access extends half-life by 10%)
```

This means:
- A memory accessed 10 times gets its half-life extended by 100% (7 days -> 14 days).
- "permanent" memories never decay.
- Memories that are never accessed fade naturally.

Decay is NOT physical deletion. Decay only affects retrieval ranking. A "maintenance path" can periodically archive or delete memories whose effective_weight falls below a threshold (e.g., 0.01).

---

## Proposed Data Flow

### Write Path (when Claude decides to remember something)

```
User says something important / Claude decides to store
  |
  v
[1] Extract fact(s) from conversation context
  |   (LLM call: "what should I remember from this?")
  |
  v
[2] Check for duplicates
  |   (vector search existing memories, threshold > 0.90)
  |   |
  |   +-> Duplicate found: UPDATE existing (merge value, boost confidence, bump updated_at)
  |   +-> No duplicate: INSERT new memory
  |
  v
[3] Score epistemic confidence
  |   (source_type + base_confidence + corroboration check)
  |
  v
[4] Generate embedding
  |   (EmbeddingEngine.encode(value) -> float32[512])
  |
  v
[5] Write to memories table + FTS5 index + embeddings table
  |
  v
[6] Topic assignment
  |   (match against topic centroids, assign or create topic)
  |
  v
[7] Causal link detection (optional, for event-type memories)
  |   (search recent memories for causal relationships)
  |
  v
[8] User profile update (if this is a user preference/fact)
      (merge into user_profile table)
```

### Read Path (when Claude needs to recall)

```
Claude receives a query / needs context
  |
  v
[1] Encode query -> embedding
  |
  v
[2] Fusion search
  |   score = w_vec * vector_sim
  |         + w_fts * fts_rank
  |         + w_time * recency_decay
  |         + w_conf * epistemic_confidence    <-- NEW
  |         + w_access * access_boost          <-- NEW
  |
  v
[3] Topic-scoped boost (optional)
  |   If we know the current topic, boost memories in same topic
  |
  v
[4] Causal chain expansion (optional)
  |   For top results, follow causal links to include related memories
  |
  v
[5] Deduplicate / merge near-duplicates in results
  |
  v
[6] Return ranked results to Claude
```

### Maintenance Path (periodic background task)

```
On session end OR periodic timer:
  |
  v
[1] Decay computation
  |   Recalculate effective_weight for all memories
  |
  v
[2] Garbage collection
  |   Archive memories with effective_weight < 0.01 for 30+ days
  |   (move to archive table or delete)
  |
  v
[3] Topic centroid recomputation
  |   Recompute centroids for topics that received new memories
  |
  v
[4] Confidence reinforcement
  |   Memories that were retrieved and used successfully -> boost confidence
  |   Memories that were retrieved but contradicted -> lower confidence
  |
  v
[5] Profile consolidation
  |   Merge redundant profile entries
  |   Resolve contradictions (newer > older, explicit > inferred)
  |
  v
[6] Causal closure table maintenance
      Rebuild closure table if edges were added/removed
```

---

## Component Boundaries

```
+-------------------------------------------------------------------+
|                        Claude Code (User)                          |
|  Calls MCP tools via conversation                                  |
+-------------------------------------------------------------------+
        |                    |                    |
        v                    v                    v
+---------------+  +------------------+  +------------------+
| vmem server   |  | evolution server |  | memory server    |
| (vmem-server) |  | (evolution-      |  | (knowledge       |
|               |  |  server.py)      |  |  graph MCP)      |
+-------+-------+  +--------+---------+  +--------+---------+
        |                    |                    |
        v                    v                    v
+-------------------------------------------------------------------+
|                    Memory Service Layer (new)                      |
|  Unified interface that all MCP servers call through               |
|                                                                    |
|  +------------------+  +------------------+  +-----------------+   |
|  | FactStore        |  | ProfileStore     |  | CausalGraph     |   |
|  | (CRUD memories)  |  | (user_profile)   |  | (causal_links   |   |
|  | + FTS5 index     |  | + key-value      |  |  + closure)     |   |
|  | + embeddings     |  | + JSON docs      |  |                 |   |
|  +------------------+  +------------------+  +-----------------+   |
|                                                                    |
|  +------------------+  +------------------+  +-----------------+   |
|  | TopicIndex       |  | ConfidenceScorer |  | DecayEngine     |   |
|  | (session_topics  |  | (epistemic +     |  | (half-life +    |   |
|  |  + centroids)    |  |  relevance)      |  |  reinforcement) |   |
|  +------------------+  +------------------+  +-----------------+   |
|                                                                    |
|  +------------------+  +------------------+                       |
|  | Deduplicator     |  | RetrievalEngine  |                       |
|  | (write-time      |  | (fusion search   |                       |
|  |  dedup)          |  |  + causal expand |                       |
|  +------------------+  +------------------+                       |
+-------------------------------------------------------------------+
        |
        v
+-------------------------------------------------------------------+
|              SQLite (single file: vmem.db / claude_memory.db)      |
|                                                                    |
|  memories          | user_profile     | causal_links               |
|  memories_fts      | sessions         | causal_closure             |
|  embeddings        | session_topics   | learning_entries           |
|  topics            | learning_patterns| memory_tags                |
+-------------------------------------------------------------------+
```

---

## Migration Path from Current System

### Phase 1: Consolidate (non-breaking)
1. Add new tables to vmem.db: user_profile, sessions, session_topics, topics, causal_links, causal_closure, learning_entries, learning_patterns
2. Copy data from evolution_memory.db -> memories table (if not already there)
3. Copy data from evolution_learning.db -> learning_entries/learning_patterns tables
4. Keep existing tables (memory_vectors, memory_fts) working
5. Add confidence, source_type columns to memory_vectors

### Phase 2: New write path
1. Implement Deduplicator (search-before-insert with 0.90 threshold)
2. Implement ConfidenceScorer (epistemic scoring at write time)
3. Implement TopicIndex (auto-assign topics on store)
4. Update vmem_store MCP tool to use new write path

### Phase 3: New read path
1. Implement DecayEngine (effective_weight computation)
2. Update fusion scoring to include confidence and access_boost
3. Implement causal chain expansion for top results
4. Update vmem_search MCP tool

### Phase 4: Maintenance
1. Implement maintenance path as a hook or periodic task
2. Implement user profile consolidation
3. Implement topic centroid recomputation
4. Archive low-weight memories

### Phase 5: Cleanup
1. Remove evolution_memory.db and evolution_learning.db (data migrated)
2. Remove memory.db (if unused)
3. Rename vmem.db -> claude_memory.db (optional)
4. Update all MCP server configs

---

## Open Questions

1. **Embedding model hot-swap**: If we switch from bge-small-zh-v1.5 to a better model, how do we handle the embeddings table? Option: store model_version alongside each embedding, re-embed lazily on access.

2. **How much should the LLM self-manage vs be managed?** MemGPT gives the LLM full control (self-editing). Mem0 does automatic extraction. Our CLAUDE.md approach is closer to Mem0 (instructions tell Claude when to write). Recommendation: keep instruction-driven writing, but add automatic deduplication and confidence scoring as a service layer that Claude does not need to think about.

3. **Reflection**: Should we implement a reflection mechanism (Stanford-style) that periodically synthesizes higher-order insights? This is essentially what the "learning patterns" table tries to do, but it is currently manual. Recommendation: implement a lightweight reflection on session end that extracts "what was the main topic, what decisions were made, what problems were solved" as a session summary memory.

4. **Causal link detection**: Manual (Claude explicitly says "this caused that") vs automatic (LLM call to infer causal relationships from temporal proximity + semantic similarity)? Recommendation: start with manual (add a causal_link MCP tool), add automatic inference later.

5. **Privacy boundary**: Everything is local SQLite. No external services. This is a hard constraint and should remain so.
