# D3 候选池 — 单表查询（SELECT 五子句 + 关系代数对应）

来源：《数据库原理与技术（SQL Server 2012）》ch05（OCR 源：`数据库原理-章节/ch05-单表查询.md`，831 行）。
行号均指 OCR 源文件行号。OCR 修复原则：引号统一为英文直引号，全角符号/错位标点修复，符号乱码按上下文推断修复。

## OCR 坏字清单（引文时已默认修复）

| 原文坏字 | 修复为 | 依据 |
|---|---|---|
| `ϱ` / `σ` 打成 `Os` / `ε` / `○`（如 "spec_NO=0201:(Student)"、`Os='0201'-(Student)`） | σ（选择算子）σ_{Spec_NO='0201'}(Student) | L81 上下文"选择运算" |
| `兀` / `元` | π（投影算子） | L85 `兀sNO,Name(Student)` |
| `SOL Server` | SQL Server | 多处页眉 |
| `SELECT 扌` | SELECT 子句 | L193 |
| `SELCET 表达式 AS 列别名` | SELECT 表达式 AS 列别名 | L237 |
| `WHEREyear（出生日期）BETWEEN1992AND1995`（引号全丢） | WHERE YEAR(出生日期) BETWEEN 1992 AND 1995 | L285 |
| `LIKE＇Photoshop CC/_2014＇ESCAPE`（'/' 错位） | LIKE 'Photoshop CC/_2014' ESCAPE '/' | L309-315 |
| `EXCEPT` 打成 `EXPECT` | EXCEPT | L417 |
| `白然连接` / `交又连接` / `册删除` | 自然连接 / 交叉连接 / 删除 | L87 / L449 / L749 |
| `HULL`（截图中 NULL 的 OCR 误读） | NULL | L321 |
| `GROUPBY`（粘连）/ `GRoUP BY` | GROUP BY | L199-203 |
| 集合函数 | 聚合（集合）函数——教材原词"集合函数"，等价于标准术语"聚集/聚合函数"，保留并注明 | L361-363 |

---

## A 类：框架候选（结构/体系）

### A1【五子句书写顺序 vs 逻辑执行顺序】★全书最大杀伤点
- 出处：L199-203（5.2.1 完整语法格式）。
- 书写顺序：SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY。
- 逻辑执行顺序（SQL 标准语义，教材通过"HAVING 从中间结果集筛选（中间结果集由 FROM、WHERE、GROUP BY 创建）"L203 间接给出链条）：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY。
- 推论（教材可证）：WHERE 先于 SELECT 执行 → WHERE 里不能用 SELECT 刚起的别名；ORDER BY 最后执行 → ORDER BY 里可以用别名。
- 考点形态：判断"WHERE 成绩别名>=80"错在哪；HAVING 能否引用 SELECT 别名。

### A2【SELECT 三大功能句型骨架】
- 出处：L193（5.2 开头）、L199。
- 骨架：`SELECT 列名表 [INTO 新表] FROM 表 [WHERE 条件] [GROUP BY 分组列] [HAVING 组条件] [ORDER BY 排序列 [ASC|DESC]]`。
- SELECT 子句=要看的列（投影）；FROM=数据来源；WHERE=要哪些行。
- 教材强调：T-SQL 中建视图、INSERT…SELECT 都依赖 SELECT，查询语句是掌握 T-SQL 的关键（L193）。

### A3【关系代数五基本操作 → SQL 对应】
- 出处：L81（选择 σ）、L85（投影 π）、L49（并/交/差）、L61（广义笛卡儿积）、L99（除）。
- 选择 σ_F(R) → WHERE；投影 π_X(R) → SELECT 列清单（投影会去重，SQL 需显式 DISTINCT——教材 L85 明说"先删除没有指明的列，然后删除重复元组"）；并/交/差 → UNION/INTERSECT/EXCEPT（L417-429）；笛卡儿积 → CROSS JOIN；除 → 无直接算子，用 NOT EXISTS 双层嵌套模拟（L651 例5.41）。
- 并、差、笛卡儿积、投影、选择构成关系运算**最小完备集**（L131）；交可用差表示 R∩S=R-(R-S)（L77）。

### A4【查询条件六大类】
- 出处：L281 表 5-23。
- 比较（= > < >= <= != <> !< !>）、范围（BETWEEN…AND / NOT BETWEEN…AND，BETWEEN 后是下限 AND 后是上限，含两端）、集合（IN / NOT IN）、字符匹配（LIKE / NOT LIKE）、空值（IS NULL / IS NOT NULL）、多重条件（AND OR NOT）。

---

## B 类：原则候选（判据/规则）

### B1【DISTINCT：去重发生在投影之后】
- 出处：L257-259（例5.9：36 条选课记录 → DISTINCT 后 7 个学号）。
- 原则：两个不相同的记录投影到部分列后可能变成相同行；DISTINCT 加在字段列表前去掉结果集中重复行。
- 钩子潜力：DISTINCT 管"列瘦身后撞脸"的行。

### B2【TOP n / TOP n PERCENT：限制返回行数】
- 出处：L263-269（例5.10：TOP 3 *）。
- TOP n=前 n 条；TOP n PERCENT=前 n%。无 ORDER BY 时"前 n 条"无确定语义（顺序=表中自然顺序）。

### B3【聚合函数对 NULL 的态度 + COUNT 三兄弟】
- 出处：L361-363（集合函数清单）、L369-371（例5.21 AVG）。
- COUNT(*)=统计记录个数（含 NULL 行）；COUNT(列)=统计该列**非空**值个数；SUM/AVG 只对数值列且忽略 NULL；MAX/MIN 忽略 NULL；默认 ALL，COUNT(DISTINCT 列) 先去重再计数。
- 教材明确"此列必须是数值型"仅限 SUM/AVG。

### B4【GROUP BY / HAVING 判据】★
- 出处：L377-383（5.2.5.2 + 例5.22）。
- 判据一：GROUP BY 把分组列值相同的记录切成一组，每组汇总出一条记录。
- 判据二（原文）："SELECT 子句的列名必须是 GROUP BY 子句已有的列名或是计算列"（L379）——非分组列不能裸出现在 SELECT。
- 判据三（原文）："HAVING 作用于组，选择满足条件的组；WHERE 作用于表，选择满足条件的记录"（L383）。
- 例5.22 本身就是 HAVING vs WHERE 陷阱例：选课人数≥4 的课程必须用 HAVING COUNT(*)>=4，因为人数是聚合后的组属性，WHERE 阶段还没有"组"。
- HAVING 前面可以没有 GROUP BY（L203），此时对整个结果集（视作一组）筛选。

### B5【IS NULL 判据：NULL 不能用 = 判断】
- 出处：L319（例5.16 原文："这里的 IS 运算符不能用 '=' 代替"）。
- NULL≠0、NULL≠空格（L319）；判断空值只能 IS NULL / IS NOT NULL。

### B6【LIKE 通配符四种 + ESCAPE 转义】
- 出处：L301-315（例5.14、5.15）。
- %：任意长度（含 0）字符串；_：任意单个字符；[ ]：括号内任一字符（支持范围 [B-E]）；[^ ]：不在括号内的任一字符。
- 匹配串本身含 % 或 _ 时用 `ESCAPE '换码字符'`，换码字符后那个通配符降级为普通字符（例5.15：'Photoshop CC/_2014' ESCAPE '/'）。

### B7【ORDER BY 规则】
- 出处：L339-347（例5.18、5.19）。
- ASC 升序（默认）/DESC 降序；多列排序：先按前面的列，值相同再按后面的列；不写 ORDER BY 时结果按表中记录顺序排列（无保证顺序）。

### B8【SELECT INTO 造表 / WHERE 1=2 造空表】
- 出处：L399-411（例5.23、5.24）。
- INTO 新表名：结果集落成新表；表名前加 # 为临时表；INTO 不能与 COMPUTE 连用；WHERE 1=2（永假条件）→ 只复制结构不复制数据。

### B9【集合查询三算子】
- 出处：L415-429（例5.25-5.27）。
- UNION（自动去重）/ UNION ALL（保留重复）/ INTERSECT / EXCEPT；参加集合操作的各结果集列数相同、对应数据类型相同；最后结果集列名来自第一个 SELECT。

---

## C 类：案例候选（书中例题，可直接进 A1）

### C1【例5.8 计算列+别名】L239-241
`SELECT 姓名, YEAR(GETDATE())-YEAR(出生日期) AS 年龄 FROM 教师` —— 表达式列必须起别名。

### C2【例5.9 DISTINCT】L257-259
`SELECT DISTINCT 学号 FROM 课程注册` —— 36 行→7 行。

### C3【例5.12 BETWEEN】L285
`WHERE YEAR(出生日期) BETWEEN 1992 AND 1995` —— 范围含两端。

### C4【例5.13 IN】L295
`WHERE 系部代码 IN ('01','02')`。

### C5【例5.14 LIKE 姓周】L303
`WHERE 姓名 LIKE '周%'`。

### C6【例5.15 ESCAPE】L309-315
`WHERE 课程名 LIKE 'Photoshop CC/_2014' ESCAPE '/'`。

### C7【例5.16 IS NULL】L319
`WHERE 备注 IS NULL`。

### C8【例5.17 多重条件】L325
`WHERE 课程号='0001' AND 成绩>=80 AND 成绩<89` —— 即 [80,89) 区间。

### C9【例5.22 GROUP BY + HAVING】★HAVING vs WHERE 陷阱例 L379-383
`SELECT 课程号,COUNT(*) AS 选课人数 FROM 课程注册 GROUP BY 课程号 HAVING COUNT(*)>=4`。

### C10【例5.25-5.27 UNION/INTERSECT/EXCEPT】L417-429
选 0001 或 0002 → UNION；既选 0001 又选 0002 → INTERSECT；选 0001 未选 0005 → EXCEPT。

---

## D 类：反例候选（错误示范/易混点）

### D1【WHERE 用 = 判 NULL】
反例：`WHERE 备注 = NULL` —— 教材 L319 明文禁止，必须 IS NULL。

### D2【WHERE 引用 SELECT 别名】
反例：`SELECT YEAR(GETDATE())-YEAR(出生日期) AS 年龄 FROM 教师 WHERE 年龄>40` —— WHERE 先于 SELECT 执行（A1 执行顺序），别名尚未诞生。正确：WHERE 里重写表达式或用 HAVING（配合 GROUP BY 时）。

### D3【聚合条件写进 WHERE】
反例：`WHERE COUNT(*)>=4` —— WHERE 作用于行，COUNT(*) 是组属性；必须 HAVING（B4/C9）。

### D4【非分组列裸奔进 SELECT】
反例：`SELECT 课程号, 学号, COUNT(*) FROM 课程注册 GROUP BY 课程号` —— 违反 B4 判据二（SELECT 列必须是分组列或聚合计算列）。

### D5【引号/通配符错配】
- 字符串必须单引号（教材全部示例如此）；BETWEEN 的低值在前高值在后（L285：BETWEEN 后是下限，AND 后是上限）。
- LIKE '周_' 只匹配姓周且名字恰好 1 个字的人——_ 是单字符不是任意串。

### D6【BETWEEN 写成两个独立条件漏 AND】
`WHERE 成绩 BETWEEN 80 AND 89` 等价于 `成绩>=80 AND 成绩<=89`（含 89）；例5.17 用 `>=80 AND <89` 是半开区间，两者不同，混用即失分。

---

## E 类：术语候选

| 术语 | 出处 | 要点 |
|---|---|---|
| 投影（Projection）π | L85 | 垂直分割，取列；自动去重（SQL 中需显式 DISTINCT） |
| 选择（Selection）σ | L81 | 水平分割，取行 |
| 连接 θ / 等值连接 / 自然连接 | L87 | 自然连接=等值连接去重复列，行列两个角度运算 |
| 除（Division） | L99 | 像集包含 S 的全部值；SQL 用 NOT EXISTS 模拟 |
| 最小完备集 | L131 | 并、差、笛卡儿积、投影、选择五操作 |
| 域/元组/分量/基数/度 | L21-29 | 度=属性数，基数=行数（练习题 3 直接考：度 7 基数 15 → 7 属性 15 行） |
| DISTINCT / TOP n [PERCENT] | L257/263 | 去重 / 限行 |
| 谓词六类 | L281 | 表 5-23 |
| 聚合（集合）函数 | L361 | COUNT/SUM/AVG/MAX/MIN |
| UNION / INTERSECT / EXCEPT | L417 | 集合查询，教材 L417 把差写作 EXCEPT（OCR 曾坏成 EXPECT） |

## 淘汰预告（进 verified.md 理由先记）
- 5.2.5.3 COMPUTE/COMPUTE BY（L389-397）：教材自己声明 SQL Server 2012 已废弃，V3' 杀伤力=0，淘汰。
- 5.1.3 关系代数等价变换规则九条（L121-125）：属查询优化理论，自考极少考到分配律细节，只保留"尽早执行选择"一句并入框架，不单独立候选。
- 5.3 连接查询全部内容、5.4 子查询全部内容：属 D4/D6 兄弟单元领地，本章只取其与单表查询的边界（B 类混淆表用），不立候选。
