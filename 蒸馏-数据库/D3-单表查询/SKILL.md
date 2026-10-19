---
name: D3-单表查询
description: |
  激活条件：题目只涉及一个表、要求写 SELECT 语句或判断 SELECT 语句正误；出现 WHERE、
  GROUP BY、HAVING、DISTINCT、TOP、ORDER BY、LIKE、IS NULL、BETWEEN、IN、聚合函数
  （COUNT/SUM/AVG/MAX/MIN）、UNION/INTERSECT/EXCEPT 等任一关键词；或问"书写顺序与
  执行顺序""WHERE 与 HAVING 区别""别名能否在 WHERE 中使用"。不调用：题目出现两个
  及以上表名或 JOIN/ON（→D4 连接查询）；出现 CREATE/ALTER/DROP TABLE（→D2 建表）；
  出现 IN(子查询)/EXISTS/ANY/ALL（→D6 子查询与函数）；纯关系代数符号推导且不落 SQL
  时仅借用本单元 σ/π 对应关系。信号：题干单表 + 五子句顺序/分组判据/NULL 判据/
  通配符/去重限行任一信号。source_book=《数据库原理与技术（SQL Server 2012）》；
  source_chapter=ch05。
---

# D3 单表查询：SELECT 五子句 + 关系代数对应

## R 关键论断

SELECT 六个子句**书写顺序固定**：SELECT→FROM→WHERE→GROUP BY→HAVING→ORDER BY；
**逻辑执行顺序不同**：FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY。
一切判据由此展开：WHERE 先于 SELECT 执行，所以 WHERE 用不了 SELECT 的列别名；
HAVING 筛的是"组"（GROUP BY 的产物），WHERE 筛的是"行"；ORDER BY 最后执行，
所以它是唯一能放心用别名的筛选/排序子句。投影（SELECT 列）对应关系代数 π，
选择（WHERE 行）对应 σ；投影天然去重，SQL 必须显式写 DISTINCT。
聚合函数里只有 COUNT(*) 看得见 NULL，其余（SUM/AVG/MAX/MIN/COUNT(列)）全部跳过 NULL；
判空唯一写法 IS NULL，等号进不去 NULL 的门。

## I 骨架 + 记忆钩子

骨架（T-SQL，方括号可选）：
```
SELECT  列清单 | * | 表达式 AS 别名 | DISTINCT 列 | TOP n [PERCENT] 列
[INTO 新表名]
FROM    表
[WHERE  行条件]
[GROUP BY 分组列清单]
[HAVING 组条件]
[ORDER BY 排序列 [ASC|DESC] [, 排序列2 [ASC|DESC]]]
```

记忆钩子（自造）：
- **"写书看目录，干活看工地"**：书写顺序是目录页（怎么写），执行顺序是施工顺序（真怎么算）。目录从 SELECT 翻起，施工从 FROM 打地基。
- **"W-G-H-S-O：胃里有食（WHERE 行）才切组（GROUP），切完卡阻（HAVING 筛组），装盘上菜（SELECT 出列），最后摆盘（ORDER BY 排序）"**——执行流水线，一步不跳。
- **"WHERE 过滤行，GROUP 切组，HAVING 卡阻"**：行→组→组淘汰，三层筛子越筛越细。
- **"WHERE 见不到 SELECT 起的名，ORDER BY 全都认"**：别名只在最后两级生效。
- **"DISTINCT 管撞脸：列瘦身后长一样的行只留一张脸"**（对应 π 投影自动去重）。
- **"IS NULL 是唯一门禁，等号进不去 NULL 的门"**。
- **"% 是随便多长，_ 只让一位站"**：通配符宽度差。
- **"UNION 并桌自动撵重客，ALL 留客；INTERSECT 找两桌都点的菜，EXCEPT 点了这桌没点那桌"**。

## A1 书中例题（至少 2 个，含 HAVING vs WHERE 陷阱）

### 例甲（原书例 5.22，HAVING vs WHERE 陷阱例）★
查询"课程注册"表中选课人数 4 人以上的各个课程号和相应选课人数：
```sql
SELECT 课程号, COUNT(*) AS 选课人数
FROM 课程注册
GROUP BY 课程号
HAVING COUNT(*) >= 4;
```
陷阱拆解：为什么不能写 `WHERE COUNT(*)>=4`？——WHERE 在 GROUP BY **之前**执行，
此刻还没有"组"，COUNT(*) 无处安放；"人数≥4"是组级属性，只能由 HAVING 卡阻。
另注意判据：SELECT 里的课程号必须出现在 GROUP BY 里（非分组列不许裸奔）。
变式陷阱：把 `COUNT(*)>=4` 改成行级条件"成绩>=80"后必须放回 WHERE——
判据："这个条件切组之前能不能对单独一行判断？"能 → WHERE，不能 → HAVING。

### 例乙（原书例 5.9，DISTINCT）
查询选修了课程的学生学号（去掉重复）：
```sql
SELECT DISTINCT 学号 FROM 课程注册;   -- 36 行 → 7 行
```
对应投影 π_学号(课程注册)：π 自动去重，SQL 必须显式 DISTINCT。
DISTINCT 对整行去重：`SELECT DISTINCT 学号, 课程号` 的去重粒度是(学号,课程号)组合。

### 例丙（原书例 5.8，表达式列 + 别名）
```sql
SELECT 姓名, YEAR(GETDATE()) - YEAR(出生日期) AS 年龄 FROM 教师;
```
表达式列必须起别名；但注意——这个"年龄"别名在 WHERE 里**不可用**（执行顺序）。

### 例丁（原书例 5.19，多列排序）
```sql
SELECT * FROM 学生 ORDER BY 班级代码 DESC, 学号 ASC;
```
先按班级代码降序，班级相同时再按学号升序——每列方向独立声明。
补充（书例 5.18）：`SELECT 学号,成绩 FROM 课程注册 WHERE 课程号='0001' ORDER BY 成绩 DESC;`
——WHERE 限行 + ORDER BY 排序的标准组合；不写 ORDER BY 时结果只是"表中自然序"。

### 例戊（原书例 5.15，ESCAPE 转义）
```sql
SELECT 课程号, 课程名 FROM 课程
WHERE 课程名 LIKE 'Photoshop CC/_2014' ESCAPE '/';
```
'/' 后的 _ 失去通配资格，按普通下划线匹配。ESCAPE 只转义**紧跟其后那一个**字符。

### 例己（原书例 5.16，空值查询）
```sql
SELECT * FROM 教师 WHERE 备注 IS NULL;
```
教材原文：IS 运算符不能用 '=' 代替。NULL ≠ 0 ≠ 空格，三者互不相同。

## A1.2 执行顺序推论三连（P1 的实战落点）

1. **推论一（WHERE × 别名）**：`SELECT 姓名, 2024-YEAR(出生日期) AS 年龄 FROM 学生 WHERE 年龄>=18` ✗——
   WHERE 在 SELECT 之前跑，"年龄"这个别名还没造出来。✓改：`WHERE 2024-YEAR(出生日期)>=18`。
2. **推论二（HAVING × 别名）**：`SELECT 课程号, COUNT(*) AS 人数 FROM 课程注册 GROUP BY 课程号 HAVING 人数>=4`——
   教材例 5.22 的标准写法是 `HAVING COUNT(*)>=4`（再聚合一次）；部分考纲接受 HAVING 用别名，考试**以聚合表达式为准**最稳。
3. **推论三（ORDER BY × 别名）**：`SELECT 姓名, YEAR(GETDATE())-YEAR(出生日期) AS 年龄 FROM 教师 ORDER BY 年龄 DESC` ✓——
   ORDER BY 最后执行，别名已存在；它还是唯一能引用 SELECT 计算列的排序出口。

## A1.3 三层筛子图（WHERE → GROUP BY → HAVING）

```
表（行堆）              WHERE 筛行            GROUP BY 切组          HAVING 卡阻
┌──────┐  不合格行 ──→  ┌──────┐  按列值相同 ──→  ┌─组1─┐  组不达标 ──→  ┌─组1─┐  SELECT 出列
│ 全部行 │  被扔掉       │ 合格行 │  切成组        │ 组2  │  整组淘汰      │ 组3  │  ORDER BY 摆盘
└──────┘              └──────┘               └─组3─┘              └─────┘
```
- WHERE 丢的是"行"（一行不合格整行出局）；HAVING 丢的是"组"（组内一人再差也不连累，看的是组指标）。
- 记忆：**WHERE 是门卫（进门查每个行），HAVING 是评委（分组演出后打分淘汰整组）**。

## A1.4 别名与表达式（书例 5.8 展开）

- 语法：`SELECT 表达式 AS 列别名 FROM 数据源`（AS 可省，考试建议保留）。
- 表达式列 = 列经运算/函数加工出来的新列：`YEAR(GETDATE())-YEAR(出生日期) AS 年龄`。
- 判据：表达式列**必须**起别名，否则结果列无名；别名只在 SELECT 之后的两级（HAVING 谨慎、ORDER BY 放心）可用。
- `*` = 全部列（书例 5.6）；部分列用英文逗号分隔且顺序可指定（书例 5.7）。

## A1.5 关系代数 ↔ SQL 对照（ch05 双主线合流）

| 关系代数 | 符号 | 方向 | SQL 落点 | 教材要害 |
|---|---|---|---|---|
| 选择 Selection | σ_F(R) | 水平（行） | WHERE 条件 | 选逻辑表达式 F 为真的元组 |
| 投影 Projection | π_X(R) | 垂直（列） | SELECT 列清单 | π **自动去重**；SQL 必须显式 DISTINCT |
| 并 Union | R∪S | 集合 | UNION（去重）/ UNION ALL | 两结果集列数、对应类型须相同 |
| 交 Intersection | R∩S | 集合 | INTERSECT | 可用差表示：R∩S = R−(R−S) |
| 差 Except | R−S | 集合 | EXCEPT | **有方向**：R−S ≠ S−R |
| 广义笛卡儿积 ECP | R×S | 集合 | CROSS JOIN | 度相加、基数相乘；结果常无意义、代价大 |
| 连接 θ / 等值 / 自然 | ⋈ | 组合 | JOIN…ON（→D4） | 自然连接=等值连接再去重复列 |
| 除 Division | R÷S | 组合 | 无直接算子（→D6 双层 NOT EXISTS） | 像集 Yx ⊇ π_Y(S) |

- 五个基本操作（并、差、笛卡儿积、投影、选择）构成关系运算**最小完备集**——判断题"交可以用差表示"出处即此。
- 除法语义一句话：**"查选了（用了/供了）全部……的……"**=像集包含题给全集，SQL 无直写算子。
- 关系基本性质四条（判断题源）：任意两行不全同；行序列序可任意交换；分量必须原子（不许"表中表"）；同列同域。
- 度=属性个数（列数），基数=元组个数（行数）。书后练习原型：度为 7、基数 15 的关系 → 7 个属性、15 行。

## A1.6 聚合函数细则（NULL 态度表）

| 函数 | 语义 | 对 NULL | 备注 |
|---|---|---|---|
| COUNT(*) | 统计记录（行）数 | **计入**含 NULL 的行 | 教材例 5.20：COUNT(*) AS 教师总数 |
| COUNT(列) | 该列非空值个数 | **跳过** | COUNT(DISTINCT 列) 先去重再数 |
| SUM(列) | 列总和 | 跳过 NULL | 列必须数值型 |
| AVG(列) | 列平均 | 跳过 NULL | 列必须数值型；例 5.21 求平均分 |
| MAX / MIN | 列最大/最小 | 跳过 NULL | 数值、日期、字符皆可 |
- 默认 ALL（不取消重复）；`COUNT(DISTINCT 学号)` 才是"有多少个不同学生"。
- 出题公式：**"某列有 k 个 NULL，COUNT(*) 与 COUNT(列) 相差 k"**。
- 除 COUNT(*) 外全部聚合都"看不见 NULL"——AVG 的分母因此比行数小，这是经典陷阱。

## A1.7 集合查询与 INTO 补例（书中例 5.23-5.27 精要）

- 并（例 5.25）：选 0001 课的学生 ∪ 选 0002 课的学生——
  ```sql
  SELECT * FROM 课程注册 WHERE 课程号='0001'
  UNION
  SELECT * FROM 课程注册 WHERE 课程号='0002'
  ORDER BY 课程号 ASC;   -- ORDER BY 对并后结果整体排序
  ```
- 交（例 5.26）：把 UNION 换成 INTERSECT，两段各 `SELECT 学号` → 既选 0001 又选 0002 的学号。
- 差（例 5.27）：换成 EXCEPT → 选了 0001 而没选 0005 的学号（方向不可反写）。
- 集合操作三判据：①各结果集列数相同；②对应列类型相容；③最终列名 = 第一个 SELECT 的列名。
- INTO 造表（例 5.23）：`SELECT * INTO 课程注册副本 FROM 课程注册;` —— 结构+数据一起复制。
- 只复制结构（例 5.24）：加永假条件 `WHERE 1=2` → 新表 0 行。表名前加 `#` 为临时表；INTO 不能与 COMPUTE 连用（COMPUTE 本身已被 SQL Server 2012 废弃，见到即排除选项）。

## A2 触发题型★（写 SQL 题的信号清单）

| 题干信号 | 对应武器 |
|---|---|
| "查询……的……信息"（单表、全行） | SELECT 列 FROM 表 |
| "不重复/去重/有哪些不同的……" | SELECT DISTINCT |
| "只要前 n 行 / 前 n%" | TOP n / TOP n PERCENT（常配 ORDER BY 才有意义） |
| "在……之间 / 某年到某年 / 成绩某区间" | BETWEEN 下限 AND 上限（含两端）或 >= AND <= |
| "属于/属于其中之一" | IN (值1, 值2, …) |
| "姓 X 的 / 包含 X 的 / 第 X 个字是……" | LIKE 'X%' / LIKE '%X%' / LIKE '_X%' |
| "……为空 / 尚无……" | IS NULL（禁用 = NULL） |
| "同时满足 / 或者 / 除外" | AND / OR / NOT（括号定优先级） |
| "每个/各/按……统计 个数/总/平均/最高/最低" | GROUP BY 分组列 + 聚合函数 |
| "统计后还要筛选组（人数≥n、平均分≥n）" | HAVING 聚合条件（绝不进 WHERE） |
| "排序输出 / 按……降序、同值按……升序" | ORDER BY 列1 [DESC], 列2 [ASC] |
| "把查询结果存成新表 / 建副本 / 只要结构" | SELECT … INTO 新表 [WHERE 1=2] |
| "选修 A 或 B 的（集合合并）" | UNION（自动去重）/ UNION ALL |
| "既选 A 又选 B" | INTERSECT；"选 A 未选 B" → EXCEPT |
| "关系代数式 σ/π 改写为 SQL" | σ→WHERE，π→SELECT（+DISTINCT） |

## E 考场步骤★（手写 SELECT 五步判据流程）

写任何单表 SELECT，按施工顺序走五步，每步带检查点：

1. **FROM 定工地**：确认只涉及一张表？出现第二个表名/JOIN → 停，移交 D4。
   检查点：题干所有字段是否都在这一张表里。
2. **WHERE 筛行**：逐个条件翻译成六类谓词（比较/BETWEEN/IN/LIKE/IS NULL/逻辑）。
   - 检查点 A：条件里有没有 SELECT 要起的别名？有 → 改写回原始表达式。
   - 检查点 B：判空只能 IS NULL / IS NOT NULL，出现 "=NULL" 直接判错。
   - 检查点 C：BETWEEN 含两端；半开区间必须拆成 >= AND <。
   - 检查点 D：条件里出现 COUNT/SUM/AVG/MAX/MIN → 报错信号，挪去 HAVING。
3. **GROUP BY 切组**：题干出现"每个/各/按……统计"才切组。
   - 检查点 E：SELECT 中每个非聚合列必须都在 GROUP BY 清单里（非分组列不许裸奔）。
4. **HAVING 卡阻**：只放"组级"条件——聚合函数结果或分组列。
   - 检查点 F：条件是针对单行字段的（如 成绩>=80）→ 应留在 WHERE，不是 HAVING。
   - 判据：先想"这个条件在切组之前能不能对一行判断？"能 → WHERE；不能 → HAVING。
5. **SELECT 出列 + ORDER BY 摆盘**：
   - 检查点 G：结果要唯一 → DISTINCT；限行 → TOP（有 ORDER BY 才保证"前 n"有义）。
   - 检查点 H：排序里每列方向独立；别名在 ORDER BY 里可用（最后执行）。

**判停条件**：五步走完，逐条回扫——① WHERE 无别名无聚合；② SELECT 非聚合列全在
GROUP BY；③ HAVING 只含聚合/分组列；④ 区间端点与题干一致；⑤ 引号全为单引号。
五条全绿 → 停笔。任何一条红 → 回到对应步骤修，不推倒重写。

## B2 六类谓词速查（WHERE 的全部弹药，原书表 5-23 重排）

| 类别 | 运算符 | 教材判据 |
|---|---|---|
| 比较 | = > < >= <= != <> !< !>（NOT 可前置求非） | <> 与 != 同义；!< 即 >=，!> 即 <= |
| 范围 | [NOT] BETWEEN 下限 AND 上限 | 下限在前上限在后，**含两端** |
| 集合 | [NOT] IN (值1, 值2, …) | 等价于一串 OR 的紧凑写法 |
| 字符匹配 | [NOT] LIKE '匹配串' | 配 % _ [ ] [^ ] 四通配符 + ESCAPE |
| 空值 | [NOT] IS NULL | **禁止 = / <> 与 NULL 比较 NULL** |
| 多重条件 | AND / OR / NOT | AND 高于 OR，拿不准就加括号 |

- IN 例（书例 5.13）：`WHERE 系部代码 IN ('01','02')` —— 01 和 02 两个系的班级。
- 逻辑组合例（书例 5.17）：`WHERE 课程号='0001' AND 成绩>=80 AND 成绩<89` —— 这写的是 [80,89) 半开区间。
- 比较例（书例 5.11）：`WHERE 成绩>=50`；范围例（书例 5.12）：`WHERE YEAR(出生日期) BETWEEN 1992 AND 1995`。
- LIKE 三件套对照：`'周%'` 姓周（例 5.14）；`'_雪%'` 第二字是雪；`'%数据库%'` 含"数据库"。`'[B-E]'` = B~E 任一字符；`'[^B]'` = 非 B 字符。

## B 边界★（失分点清单 + 混淆表）

### 失分点清单
1. WHERE 引用 SELECT 别名（执行顺序：别名未诞生）。
2. 聚合条件写进 WHERE（`WHERE COUNT(*)>=4` 非法）。
3. 行级条件误写进 HAVING（HAVING 筛组不筛行，能写 WHERE 的别写 HAVING）。
4. 非分组列裸奔进 SELECT（SELECT 列 ⊆ GROUP BY 列 ∪ 聚合计算列）。
5. `= NULL` / `<> NULL`（必须 IS NULL / IS NOT NULL）。
6. 单引号/双引号互换：T-SQL 字符串一律单引号，双引号是标识符——考试写双引号即扣分。
7. BETWEEN 端点：BETWEEN 80 AND 89 含 89；题干"[80,89)"要拆 >=80 AND <89。
8. LIKE 中 _ 当"任意串"用（它是单字符）；含 %/_ 的字面串忘 ESCAPE。
9. UNION 自动去重、UNION ALL 才保留重复；结果列名取自第一个 SELECT。
10. TOP n 不配 ORDER BY 时"前 n 条"无意义（表中自然序，不保证）。
11. COUNT(*) 与 COUNT(列)：前者计整行（含 NULL 行），后者跳过 NULL；SUM/AVG 忽略 NULL 且仅数值列。
12. DISTINCT 是对整个结果行去重，不是对某一列去重。

### 与兄弟单元混淆表
| 症状 | 归属 | 分界判据 |
|---|---|---|
| FROM 出现两个表 / JOIN…ON / WHERE 里写 表1.列=表2.列 | D4 连接查询 | 有第二个表名就不是单表查询 |
| 笛卡儿积、自身连接、外连接 NULL 填充 | D4 | 多表行组合问题 |
| IN (SELECT …)、EXISTS、ANY/ALL、相关子查询 | D6 子查询 | 括号里藏 SELECT |
| YEAR()/GETDATE() 等函数本身的坑（如对 NULL 求年份） | D6 函数陷阱 | 单表查询只管函数当表达式列用，不研究函数内部陷阱 |
| CREATE TABLE / ALTER / 数据类型 / 约束 | D2 DDL | 建表改表不是查询 |
| 关系代数除法（"选修全部课程"型） | D6 | SQL 落地用双层 NOT EXISTS，非单表五子句能表达 |

### 单元一句话边界
**只有一张表 + 五子句（可带集合算子）= D3；多表 = D4；嵌套查询块 = D6。**

### 优先级与自检附录（考场最后 30 秒）
- 逻辑运算优先级：NOT > AND > OR；比较运算高于逻辑运算。
- 单引号内再出现单引号：T-SQL 考试层面避开这种写法，改用不含引号的匹配串。
- 自检三问：①别名是否只出现在 ORDER BY？②聚合是否只出现在 SELECT/HAVING？③每个 SELECT 非聚合列是否都在 GROUP BY？三问全"是"才交卷。
- TOP 与 DISTINCT 同用时写法：`SELECT DISTINCT TOP 3 学号 FROM …`——T-SQL 允许 TOP 紧跟 DISTINCT 之后（TOP n 在 DISTINCT 后、列前），考试以教材句型 `SELECT TOP 3 * FROM 表` 为准。

## 审计信息

- source_book: 《数据库原理与技术（SQL Server 2012）》
- source_chapter: ch05（5.1 关系运算 / 5.2 单表查询为主；5.3、5.4 仅作边界）
- 源文件: `数据库原理-章节/ch05-单表查询.md`（OCR，831 行，坏字修复记录见 candidates.md）
- 产出流程: candidates.md（五候选池）→ verified.md（V1/V2/V3' 三重验证，10 通过 3 淘汰）→ 本文件
- OCR 修复声明: ϱ/Os/ε/○→σ、兀/元→π、SOL→SQL、EXPECT→EXCEPT、SELECT扌/SELCET→SELECT、
  全角引号→直引号、白然→自然、交又→交叉 等；引文均按上下文修复后引用。
- 行数: 本文件 1 行 frontmatter 描述块 + 正文，总计 ≤220 行。
