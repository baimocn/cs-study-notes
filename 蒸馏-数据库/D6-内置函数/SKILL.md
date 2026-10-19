---
name: D6-内置函数
description: SQL Server 内置函数考场蒸馏。统一判据：函数题只考"输入啥→返回啥"，尤其对 NULL 怎么办。覆盖聚合（COUNT(*)/COUNT(列)/AVG/SUM/MAX/MIN 对 NULL 的差异）、字符串（LEN/CHARINDEX/CONCAT 的 NULL 当空串）、日期（YEAR/MONTH/DAY 返回 int、EOMONTH 取月末）、数学（CEILING/FLOOR/ROUND 负数方向）、转换（CAST 语法、TRY_CONVERT 失败返 NULL）。含书中例8.1~8.31 全部返回值帧、填空/选择触发信号、失分点边界与 D3 分工混淆表。源自《数据库原理与技术（SQL Server 2012）》ch08。
source_book: 数据库原理与技术（SQL Server 2012）
source_chapter: ch08
unit: D6
---

# D6 内置函数

## R（引用）

> 来源：ch08 §8.1。OCR 修复后引文：「SQLServer 提供了内置函数帮助用户执行各种操作。内置函数不能修改，可以在 T-SQL 语句中使用。内置函数包括：聚合函数、配置函数、加密函数、游标函数、时间和日期函数、数学函数、元数据函数、排名函数、行集函数、安全函数、字符串函数、系统函数、系统统计函数、文本和图像函数等。」
> 审计：原文"SQLServer"补空格；§8.1.1 参数描述中"返回唯一非空值的数量"系 OCR 错复制给 MAX/MIN/SUM，frames 中已按 DISTINCT 正确语义（去重后计算）修复。

## I（骨架 + 钩子）

统一判据：**内置函数题=输入啥→返回啥，外加一条——参数里混进 NULL 会怎样。**
四类全走同一问法，答题就是逐帧对答案：

```
内置函数（输入→返回值）
├─ 聚合：多行进 → 单值出        核心钩子：聚合怕 NULL——先问"NULL 行算不算"
│   COUNT(*)≠COUNT(列)：*数行、列数非空值
├─ 字符串：字符串进 → 串/数出   核心钩子：CONCAT 把 NULL 当空串；CHARINDEX 找不到=0
├─ 日期：日期进 → int/串/日期出 核心钩子：YEAR/MONTH/DAY 返回 int，DATENAME 返回字符串
├─ 数学：数进 → 数出            核心钩子：CEILING 向大、FLOOR 向小，负数不反转
└─ 转换：类型搬家               核心钩子：CAST('123' AS int)；TRY_CONVERT 失败返 NULL
```

记忆锚：**聚合怕 NULL，字符串怕空格（LEN 不算尾随空格），日期分 int/串，转换怕失败（TRY_CONVERT 兜底 NULL）。**

## A1（书中函数例题 → 返回值帧）

| # | 问题（书例） | 函数 | 输入→返回值 |
|---|---|---|---|
| 1 | 统计每生平均成绩（例8.1） | AVG+GROUP BY | AVG(课程注册.成绩) 按学号分组→每生均值；忽略 NULL 成绩行 |
| 2 | 统计每生选课数（例8.2） | COUNT(DISTINCT 列) | COUNT(DISTINCT 课程号)→去重后非空课程数（防重复选课记录） |
| 3 | 每门课最高分学生（例8.3） | MAX+子查询 | MAX(成绩)→最高分；WHERE 成绩 IN (SELECT MAX(成绩)…) 捞行 |
| 4 | LEFT 截取（例8.26） | LEFT(str,x) | LEFT('command',4)→'comm' |
| 5 | 姓名含"雪"或"梅"（例8.27） | CHARINDEX | CHARINDEX('雪',姓名)>0 即命中；找不到返回 0 |
| 6 | 通配符找位置（例8.28） | PATINDEX | PATINDEX('%tt%','wwttyy')→3 |
| 7 | NULL 参与连接（例8.29） | CONCAT | CONCAT('hello',NULL,'world')→'helloworld'（NULL 当空串） |
| 8 | 系统日期（例8.6） | GETDATE() | →'2017-01-15 22:38:16.333'（datetime） |
| 9 | 取日/月/年（例8.7-8.9） | DAY/MONTH/YEAR | DAY('01/15/2017')→15；MONTH→1；YEAR→2017（全 int） |
| 10 | 拼日期（例8.10） | DATEFROMPARTS | (2017,1,15)→'2017-01-15' |
| 11 | 月末（例8.13） | EOMONTH | EOMONTH('2017-01-16')→'2017-01-31'；EOMONTH(…,1)→'2017-02-28' |
| 12 | 绝对值（例8.15） | ABS | ABS(-12)→12 |
| 13 | 取整方向（例8.17/8.19） | CEILING/FLOOR | CEILING(56.3)→57，CEILING(-56.3)→-56；FLOOR(56.3)→56，FLOOR(-56.3)→-57 |
| 14 | 四舍五入（例8.21） | ROUND | ROUND(56.34,1)→56.30；ROUND(56.34,-1)→60（y 负=小数点左侧） |
| 15 | 幂/平方/开方（例8.20-8.23） | POWER/SQUARE/SQRT | POWER(2,3)→8；SQUARE(5)→25；SQRT(16)→4 |
| 16 | 字符串转 int（例8.31） | CAST | CAST('123' AS int)+20→143 |
| 17 | 转换失败兜底（例8.35） | TRY_CONVERT | TRY_CONVERT(float,'ttt')→NULL（不报错） |
| 18 | 按索引取值（例8.36） | CHOOSE | CHOOSE(3,'A','B','C','D')→'C'（1 起数） |
| 19 | 布尔二选一（例8.37） | IIF | IIF(3>2,'T','F')→'T' |

## 速查表（考场 30 秒版，本单元钩子的最终形态）

| 函数 | 输入→返回值 | NULL/陷阱 |
|---|---|---|
| COUNT(*) | 全表行数 | 含 NULL 行；空表=0；永不返 NULL |
| COUNT(列) | 该列非 NULL 值个数 | 跳过 NULL |
| COUNT(DISTINCT 列) | 去重后非空个数 | 例8.2 防重复 |
| SUM / AVG / MAX / MIN | 非空值求和/均值/最大/最小 | 跳过 NULL；空集返 NULL 不是 0 |
| SUM(DISTINCT 列) | 去重后求和 | 相同值只加一次 |
| LEN(str) | 字符个数 | 不含尾随空格：LEN('abc ')→3 |
| LEFT/RIGHT(str,x) | 左/右起 x 个字符 | LEFT('command',4)→'comm' |
| SUBSTRING(str,start,len) | 从 start 起长 len 的子串 | 位置从 1 起 |
| CHARINDEX(s1,s2) | s1 在 s2 中的位置 | 找到>0，找不到=0 |
| PATINDEX('%s%',s2) | 同上但支持通配符 | PATINDEX('%tt%','wwttyy')→3 |
| REPLACE(s1,s2,s3) | s1 里的 s2 全换成 s3 | |
| UPPER / LOWER | 大写 / 小写 | 返 varchar |
| LTRIM / RTRIM | 删起始 / 尾随空格 | |
| CONCAT(a,b,…) | 连接各串 | **NULL 当空串**：'hello'+NULL+'world'→helloworld |
| GETDATE() | 当前系统日期时间 | datetime，带毫秒 |
| YEAR / MONTH / DAY(d) | 年 / 月 / 日的整数 | **返回 int** |
| DATENAME(part,d) | 日期指定部分的字符串 | weekday('12/20/2016')→'星期二' |
| DATEFROMPARTS(y,m,d) | 拼出日期 | (2017,1,15)→'2017-01-15' |
| EOMONTH(d[,n]) | d 所在月（+n 月）最后一天 | EOMONTH('2017-01-16',1)→'2017-02-28' |
| ABS(x) | 绝对值 | ABS(-12)→12 |
| CEILING(x) | ≥x 的最小整数 | CEILING(-56.3)→-56（向大） |
| FLOOR(x) | ≤x 的最大整数 | FLOOR(-56.3)→-57（向小） |
| ROUND(x,y) | 按 y 精度四舍五入 | y 负=小数点左侧：ROUND(56.34,-1)→60 |
| POWER(x,y) / SQUARE(x) / SQRT(x) | x^y / x² / √x | 8 / 25 / 4 |
| CAST(e AS type) | 类型转换 | CAST('123' AS int)+20→143 |
| CONVERT(type,e[,style]) | 同 CAST，多 style 管日期格式 | style=23 → 'yyyy-mm-dd' |
| TRY_CONVERT(type,e) | 转换失败返 NULL 不报错 | TRY_CONVERT(float,'ttt')→NULL |
| CHOOSE(i,v1,v2,…) | 第 i 个列表项（1 起） | CHOOSE(3,'A','B','C','D')→'C' |
| IIF(条件,a,b) | 真取 a 假取 b | IIF(3>2,'T','F')→'T' |

## A2（触发题型★）

**填空题信号**——题面直接给函数调用，让填返回值：
- "SELECT ROUND(56.34,-1) 的结果是____"→60
- "SELECT CONCAT('hello',NULL,'world') 的结果是____"→helloworld
- "SELECT YEAR('01/15/2017') 的结果是____"→2017
- "SELECT SQRT(16) 的结果是____"→4

**选择题信号**——比差异：
- COUNT(*) vs COUNT(成绩)：前者数所有行（含 NULL 行），后者只数非 NULL 值 → 5 行成绩含 1 个 NULL 时，COUNT(*)=5，COUNT(成绩)=4
- CHARINDEX vs PATINDEX：后者支持 % 通配符
- CAST vs CONVERT：CONVERT 多 style 参数管日期格式
- TRY_CONVERT vs CONVERT：转换失败前者返 NULL、后者报错

## E（考场步骤）

见到函数题，三步逐帧判：
1. **认类**：聚合/字符串/日期/数学/转换，对号入座。
2. **问 NULL**：参数列里有没有 NULL？聚合先想"NULL 算不算"（COUNT(*) 算行、其余聚合跳过 NULL、CONCAT 把 NULL 当空串）；转换先想"转不动会怎样"（TRY_CONVERT→NULL）。
3. **对返回类型**：日期族 YEAR/MONTH/DAY 返 int、DATENAME 返字符串；数学族 CEILING/FLOOR 负数方向别反；SUBSTRING(str,start,len) 记"位置+长度"两个参数。

## B（边界★失分点）

- **SUM/AVG 空集返回 NULL，不是 0**——教材未明说，属 SQL 标准行为；只有 COUNT 空表返回 0，COUNT(*) 永不返回 NULL。答"空表求和=0"是典型失分。
- LEN 不计尾随空格：LEN('abc ')→3。
- CEILING(-56.3)→-56（向大），FLOOR(-56.3)→-57（向小）——负数方向最容易反。
- AVG 忽略 NULL：5 行成绩 1 个 NULL，AVG 分母是 4 不是 5。
- **D3/D6 分工混淆表**：

| 症状 | 归属 | 口诀 |
|---|---|---|
| WHERE/GROUP BY/HAVING 怎么排、子查询怎么嵌 | D3 单表查询五子句 | "查的骨架问 D3" |
| AVG/COUNT 出现在 SELECT 列表/HAVING 里对 NULL 的处理 | D6 本单元 | "函数返回值问 D6" |
| 多表 JOIN 条件 | D4 连接 | "表怎么拼问 D4" |
| DECLARE @x、流程控制、自定义函数语法 | D7 T-SQL | "变量和 BEGIN..END 问 D7" |

- 术语降级区（只认名字，不出帧）：配置函数（@@VERSION）、元数据函数（COL_LENGTH）、排名函数（RANK 并列跳号 / ROW_NUMBER 连续编号）、三角对数指数函数。

## 自测五连（遮住右列答）

| 题面 | 答案 |
|---|---|
| 表 5 行成绩，1 行 NULL：COUNT(*)、COUNT(成绩)、AVG(成绩) 的分母各是多少？ | 5、4、4（AVG 分母是非空行数） |
| SELECT COUNT(*) FROM 空表；SELECT SUM(成绩) FROM 空表 | 0；NULL（不是 0） |
| LEN('abc ')、CEILING(-3.2)、FLOOR(3.8) | 3；-3；3 |
| CONCAT('a',NULL,'b') 与 'a'+NULL+'b' 的差别 | CONCAT→'ab'（NULL 当空串）；+ 拼接遇 NULL→NULL |
| CAST('123' AS int)+20 与 TRY_CONVERT(float,'ttt') | 143；NULL |

## 审计信息

- 来源：数据库原理-章节/ch08-内置函数.md（OCR 损伤较重，已修复）
- OCR 坏字清单：`AVGO`→AVG()、`COUNTO`→COUNT()、`MAXO`→MAX()、`flo0r`→FLOOR、`COL LENGTH`→COL_LENGTH、`@@SERVE- RNAME`→@@SERVICENAME+@@SERVERNAME 拼版错乱、`DISCTINCT`→DISTINCT、MIN 定义误印"最大值"（已按"最小值"修正）
- 教材错置：§8.2~8.4 用户定义函数/标量函数/表值函数不属内置函数，未收录本单元
- 验证记录：verified.md（C1-C5 全过 V1/V2/V3'，C4 标注单小节支撑）
