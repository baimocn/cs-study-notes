# -*- coding: utf-8 -*-
"""schema 归一化：dump 分类字段取值分布 + 统一抽取"""
import json, os, collections

ROOT = r"D:\Desktop\计算机科学与技术"
VOLS = {
    "数据库": os.path.join(ROOT, "蒸馏-数据库"),
    "高级语言": os.path.join(ROOT, "蒸馏-高级语言"),
}
TMP = os.path.join(ROOT, ".workbuddy", "tmp")

TRIGGER_KEYS = {"should_trigger", "test_prompts", "triggers", "cases", "prompts", "items"}
DECOY_KEYS = {"should_not_trigger", "decoy", "decoys", "distractors", "bait_prompts"}
EDGE_KEYS = {"edge", "edge_case", "edges", "edge_prompts"}

lines = []
for vol, d in VOLS.items():
    lines.append(f"=== {vol} ===")
    for u in sorted(os.listdir(d)):
        p = os.path.join(d, u, "test-prompts.json")
        if not os.path.isdir(os.path.join(d, u)) or not os.path.exists(p):
            continue
        data = json.load(open(p, encoding="utf-8"))
        lines.append(f"  {u}")
        for k, v in data.items():
            if not isinstance(v, list) or not (v and isinstance(v[0], dict)):
                continue
            # 分类字段的取值分布
            for cf in ("type", "question_type", "kind", "category", "skill", "tag", "stars", "difficulty"):
                if cf in v[0]:
                    cnt = collections.Counter(str(i.get(cf)) for i in v)
                    lines.append(f"    {k}: {cf} -> {dict(cnt)}")
                    break

open(os.path.join(TMP, "dist.txt"), "w", encoding="utf-8").write("\n".join(lines))

# ---- 统一抽取 ----
unified = {}
for vol, d in VOLS.items():
    units = []
    for u in sorted(os.listdir(d)):
        p = os.path.join(d, u, "test-prompts.json")
        if not os.path.isdir(os.path.join(d, u)) or not os.path.exists(p):
            continue
        data = json.load(open(p, encoding="utf-8"))
        rec = {"unit": u, "trig": [], "decoy": [], "edge": []}
        for k, v in data.items():
            if not isinstance(v, list) or not (v and isinstance(v[0], dict)):
                continue
            bucket = None
            if k in TRIGGER_KEYS:
                bucket = "trig"
            elif k in DECOY_KEYS:
                bucket = "decoy"
            elif k in EDGE_KEYS:
                bucket = "edge"
            if bucket is None:
                continue
            for i, item in enumerate(v):
                q = (item.get("prompt") or item.get("question") or item.get("stem") or "")
                a = (item.get("expected_behavior") or item.get("answer")
                     or item.get("reference_answer") or item.get("expected_answer") or "")
                tp = (item.get("type") or item.get("question_type")
                      or item.get("kind") or item.get("category") or "")
                kps = item.get("key_points") or []
                if isinstance(kps, str):
                    kps = [kps]
                hook = (item.get("hook") or item.get("point") or item.get("anchor") or "")
                rec[bucket].append({
                    "id": item.get("id") or f"{u}-{k}-{i+1:02d}",
                    "type": tp,
                    "q": q,
                    "a": a,
                    "kp": kps,
                    "hook": hook,
                    "src_key": k,
                })
        units.append(rec)
    unified[vol] = units

json.dump(unified, open(os.path.join(TMP, "unified.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 统计
print("ok")
