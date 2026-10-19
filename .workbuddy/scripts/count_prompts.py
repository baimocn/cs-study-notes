# -*- coding: utf-8 -*-
"""统计两卷蒸馏题库的触发题/诱饵/边界分布"""
import json, os, sys

ROOT = r"D:\Desktop\计算机科学与技术"
VOLS = {
    "数据库": os.path.join(ROOT, "蒸馏-数据库"),
    "高级语言": os.path.join(ROOT, "蒸馏-高级语言"),
}

OUT = os.path.join(ROOT, ".workbuddy", "tmp", "count.txt")
lines = []
def say(s=""):
    lines.append(s)

grand = {}
for vol, d in VOLS.items():
    units = sorted([x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))])
    tot_t = tot_n = tot_e = 0
    say(f"=== {vol} ===")
    for u in units:
        p = os.path.join(d, u, "test-prompts.json")
        if not os.path.exists(p):
            say(f"  [MISS] {u}")
            continue
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        t = len(data.get("should_trigger", []))
        n = len(data.get("should_not_trigger", []))
        e = len(data.get("edge_case", []))
        tot_t += t; tot_n += n; tot_e += e
        types = sorted({i.get("type", "?") for i in data.get("should_trigger", [])})
        maxlen = max((len(i.get("prompt", "")) for i in data.get("should_trigger", [])), default=0)
        say(f"  {u:30s} 触发{t:2d} 诱饵{n} 边界{e}  最长题干{maxlen}字  型: {'/'.join(types)}")
    say(f"  --> 合计 触发{tot_t} 诱饵{tot_n} 边界{tot_e}")
    grand[vol] = (tot_t, tot_n, tot_e)

say("")
say("=== 总览 ===")
say(f"触发题合计: {sum(v[0] for v in grand.values())}")
say(f"诱饵题合计: {sum(v[1] for v in grand.values())}")
say(f"边界题合计: {sum(v[2] for v in grand.values())}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("done")

