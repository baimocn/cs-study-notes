# -*- coding: utf-8 -*-
"""生成两卷记忆账本（修正版：按 item.type 细分 trigger/decoy/edge）"""
import json, os, re

ROOT = r"D:\Desktop\计算机科学与技术"
TMP = os.path.join(ROOT, ".workbuddy", "tmp")

VOLS = [
    ("数据库系统原理", "蒸馏-数据库", "记忆账本-数据库.md",
     "《数据库原理与技术（SQL Server 2012）》"),
    ("高级语言程序设计", "蒸馏-高级语言", "记忆账本-高级语言.md",
     "《高级语言程序设计（2017年版）》"),
]

TRIGGER_KEYS = {"should_trigger", "test_prompts", "triggers", "cases", "prompts", "items"}
DECOY_KEYS = {"should_not_trigger", "decoy", "decoys", "distractors", "bait_prompts"}
EDGE_KEYS = {"edge", "edge_case", "edges", "edge_prompts"}


def classify(item, default):
    tv = str(item.get("type") or item.get("question_type") or item.get("kind")
             or item.get("category") or "").lower()
    if ("should_not_trigger" in tv or "decoy" in tv or "bait" in tv
            or "distractor" in tv or "诱饵" in tv or "应指向" in tv
            or "confusable" in tv):
        return "decoy"
    if tv.startswith("edge") or "edge-" in tv or tv in ("edge", "边界", "edge_case"):
        return "edge"
    if tv in ("should_trigger", "trigger"):
        return "trig"
    return default


def get(item, *keys):
    for k in keys:
        v = item.get(k)
        if v:
            return v
    return ""


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


CLASS_MARK = {"should_trigger", "trigger", "decoy", "edge", "should_not_trigger", "edge_case"}
TYPE_MAP = {
    "short_answer": "简答", "judge_with_reason": "判断说理",
    "multiple_choice": "选择", "single_choice": "选择", "choice": "选择",
    "fill-blank": "填空", "fill_blank": "填空",
    "read_output": "读程序写结果", "read_program": "读程序写结果",
}

# D4 / D7 的 json 未带题型字段，按题面人工核定
FIX_TYPE = {
    "D4-ODBC-01": "选择", "D4-JOIN-02": "应用", "D4-JOIN-03": "简答",
    "D4-ADO-04": "简答", "D4-ODBC-05": "判断+简答", "D4-JOIN-06": "简答",
    "D7-01": "简答", "D7-02": "简答", "D7-03": "编程", "D7-04": "判断",
    "D7-05": "编程", "D7-06": "填空/简答", "D7-07": "简答", "D7-08": "简答",
    "C1-T01": "计算", "C1-T02": "计算", "C1-T03": "计算", "C1-T04": "计算",
    "C1-T05": "计算", "C1-T06": "辨析", "C1-T07": "计算", "C1-T08": "计算",
}


def type_of(item):
    tp = get(item, "type", "question_type", "kind", "category") or ""
    if str(tp).lower() in CLASS_MARK:
        tp = get(item, "question_type") or ""
    if not tp:
        return "—"
    return TYPE_MAP.get(str(tp), str(tp))


def brief(q, n=42):
    q = re.sub(r"\s+", " ", str(q)).strip()
    for pre in ("判断题：", "判断下列语句是否正确并说明理由：", "判断题（", "填空：", "简答："):
        if q.startswith(pre):
            q = q[len(pre):]
    return q[:n] + ("…" if len(q) > n else "")


def hook_of(item):
    kp = item.get("kp") or []
    if isinstance(kp, str):
        kp = [kp]
    if kp:
        return "；".join(str(x) for x in kp[:2])
    h = get(item, "hook", "point", "anchor")
    if h:
        return str(h)
    a = get(item, "a")
    a = re.sub(r"^(答出|答|正确|错误|判错并纠正|不|不能)[：:，,]?\s*", "", str(a))
    a = a.lstrip("。，、：； ")
    if len(a) < 8:
        e = get(item, "explanation", "notes")
        if e:
            a = re.sub(r"\s+", " ", str(e))
    return a[:78]


def tag_of(item):
    for k in ("tag", "difficulty", "stars"):
        v = item.get(k)
        if v is None or str(v).strip() == "":
            continue
        s = str(v).strip()
        return "★" * int(s) if s.isdigit() else s
    return "—"


def collect(vol_dir):
    units = []
    for u in sorted(os.listdir(vol_dir)):
        p = os.path.join(vol_dir, u, "test-prompts.json")
        if not os.path.isdir(os.path.join(vol_dir, u)) or not os.path.exists(p):
            continue
        data = json.load(open(p, encoding="utf-8"))
        rec = {"unit": u, "trig": [], "decoy": [], "edge": []}
        for k, v in data.items():
            if not isinstance(v, list) or not (v and isinstance(v[0], dict)):
                continue
            if k in TRIGGER_KEYS:
                default = "trig"
            elif k in DECOY_KEYS:
                default = "decoy"
            elif k in EDGE_KEYS:
                default = "edge"
            else:
                continue
            for i, item in enumerate(v):
                b = classify(item, default)
                q = get(item, "prompt", "question", "stem", "surface")
                a = get(item, "expected_behavior", "answer",
                                          "reference_answer", "expected_answer", "correct_answer")
                tp = type_of(item)
                kp = item.get("key_points") or []
                if isinstance(kp, str):
                    kp = [kp]
                rec[b].append({
                    "id": get(item, "id") or f"{u}-{k}-{i+1:02d}",
                    "q": q, "a": a, "type": tp, "kp": kp,
                    "hook": get(item, "hook", "point", "anchor"),
                    "explanation": get(item, "explanation"),
                    "notes": get(item, "notes"),
                    "tag": item.get("tag") or item.get("difficulty") or item.get("stars"),
                    "rawtype": get(item, "type", "question_type", "kind", "category"),
                    "src": k,
                })
        # id 统一：凡不以单元短名开头、或由容器名自动生成的一律重编号，保证全库唯一
        short = rec["unit"].split("-")[0]
        for b, pre in (("trig", "T"), ("decoy", "D"), ("edge", "E")):
            for i, x in enumerate(rec[b], 1):
                sid = str(x["id"]).strip()
                if (not sid.upper().startswith(short.upper() + "-")
                        or re.search(r"-(prompts|cases|items)-", sid)):
                    x["id"] = f"{short}-{pre}{i:02d}"
        units.append(rec)
    return units


for vol_name, vol_dir_name, out_name, book in VOLS:
    units = collect(os.path.join(ROOT, vol_dir_name))
    T = sum(len(u["trig"]) for u in units)
    D = sum(len(u["decoy"]) for u in units)
    E = sum(len(u["edge"]) for u in units)

    L = []
    L.append(f"# {vol_name} · 记忆账本")
    L.append("")
    L.append("> **规则**：答错记下来，隔几分钟 / 隔天再问，**连续两次答对才划账**（连对两次才进「已过关」）。")
    L.append(f"> **来源**：`{vol_dir_name}\\`（{book}）· 初始化 2026-09-13")
    L.append(f"> **口径**：触发题 {T} 道 / 诱饵 {D} 道 / 边界 {E} 道")
    L.append("> **选题公式**：优先级 = 错次×3 + 距今×1 + 标签×2（标签在抽测中标注：高频 / 易错 / 概念混淆）")
    L.append("> **状态**：⬜ 未测 · 🔴 待复测（错过）· 🟢 已过关（连对两次）")
    L.append("")
    L.append("## 总览")
    L.append("")
    L.append("| 单元 | 触发 | ⬜未测 | 🔴待复测 | 🟢已过关 |")
    L.append("|---|---|---|---|---|")
    for u in units:
        n = len(u["trig"])
        L.append(f"| {u['unit']} | {n} | {n} | 0 | 0 |")
    L.append(f"| **合计** | **{T}** | **{T}** | **0** | **0** |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 待测池（按学习顺序，抽测后回填状态）")
    L.append("")
    for u in units:
        L.append(f"### {u['unit']}（{len(u['trig'])} 题）")
        L.append("")
        L.append("| 题号 | 型 | 题眼 | 判据钩子 | 标签 | 错次 | 最近测 | 状态 |")
        L.append("|---|---|---|---|---|---|---|---|")
        for x in u["trig"]:
            L.append("| {} | {} | {} | {} | {} | 0 | — | ⬜ |".format(
                esc(x["id"]), esc(FIX_TYPE.get(x["id"], x["type"])), esc(brief(x["q"])),
                esc(hook_of(x)), esc(tag_of(x))))
        L.append("")

    L.append("---")
    L.append("")
    L.append("## 诱饵池（**不应**由本单元作答，抽测时用来验边界）")
    L.append("")
    for u in units:
        if not u["decoy"]:
            continue
        me = u["unit"].split("-")[0]
        L.append(f"**{u['unit']}**")
        L.append("")
        for x in u["decoy"]:
            tgt = ""
            txt = " ".join(str(x.get(k) or "") for k in ("rawtype", "a", "explanation", "notes"))
            nums = re.findall(r"([CD]\d)", txt)
            others = [n for n in nums if n != me]
            if others:
                tgt = f" → 指向 {others[0]}"
            L.append(f"- `{esc(x['id'])}` {esc(brief(x['q'], 50))}{tgt}")
        L.append("")

    L.append("## 边界池（双重归属，部分通过算过关）")
    L.append("")
    for u in units:
        if not u["edge"]:
            continue
        L.append(f"**{u['unit']}**")
        L.append("")
        for x in u["edge"]:
            L.append(f"- `{esc(x['id'])}` {esc(brief(x['q'], 60))}")
        L.append("")
    L.append("---")
    L.append("")
    L.append("*初始化：2026-09-13 · 抽测后请把 ⬜ 改为 🔴 / 🟢，并回填错次与最近测日期。*")

    open(os.path.join(ROOT, out_name), "w", encoding="utf-8").write("\n".join(L))
    print(vol_name, T, D, E)
