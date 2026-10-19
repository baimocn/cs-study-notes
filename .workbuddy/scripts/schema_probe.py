# -*- coding: utf-8 -*-
"""探测 17 个 test-prompts.json 的 schema 差异"""
import json, os

ROOT = r"D:\Desktop\计算机科学与技术"
VOLS = {
    "数据库": os.path.join(ROOT, "蒸馏-数据库"),
    "高级语言": os.path.join(ROOT, "蒸馏-高级语言"),
}
OUT = os.path.join(ROOT, ".workbuddy", "tmp", "schema.txt")
lines = []

for vol, d in VOLS.items():
    lines.append(f"=== {vol} ===")
    for u in sorted(os.listdir(d)):
        p = os.path.join(d, u, "test-prompts.json")
        if not os.path.isdir(os.path.join(d, u)) or not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        tops = list(data.keys())
        # 找出数组型 key 及其长度、首元素 key
        arrs = []
        for k, v in data.items():
            if isinstance(v, list):
                itemkeys = sorted(v[0].keys()) if v and isinstance(v[0], dict) else []
                arrs.append(f"{k}({len(v)})[{','.join(itemkeys)}]")
        lines.append(f"  {u}")
        lines.append(f"    top: {','.join(tops)}")
        lines.append(f"    arr: {' | '.join(arrs)}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("done")
