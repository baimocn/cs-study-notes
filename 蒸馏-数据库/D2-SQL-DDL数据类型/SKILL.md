---
name: D2-SQL-DDL数据类型
description: 当需要建库建表写 DDL 语句（CREATE/ALTER/DROP DATABASE 或 TABLE）、为字段选 SQL Server 数据类型（char/varchar/nchar、int 系、decimal、money、datetime、bit、IDENTITY）、回答文件类型/文件组/页存储/系统数据库相关考题时激活。覆盖《数据库原理与技术（SQL Server 2012）》ch03 数据库基本操作与 ch04 表基本操作中的 DDL 与数据类型考点；不覆盖完整性约束语义（D1）与查询语句（D3）。
source_book: 《数据库原理与技术（SQL Server 2012）》
source_chapter: ch03+ch04
---

# D2 · SQL DDL 与数据类型

## R 关键论断（引文）

> 「数据类型是用来表现数据特征的，它决定了数据在计算机中的存储格式、存储长度、数据精度和小数位数等属性。在创建 SQL Server 表时，表中的每一列必须确定列的数据类型，确定了数据类型也就确定了该列数据的取值范围。」（ch04 §4.1.2）

> 「一个数据库至少应包含一个数据文件和一个事务日志文件……主要数据文件……每个数据库都必须有而且只能有一个……扩展名为 .mdf……事务日志文件……至少必须有一个……扩展名为 .ldf。」（ch03 §3.1.3）

> 「一页是一块 8KB（8×1024B，其中用 8060B 存储数据，另外的 132B 存放系统信息）的连续磁盘空间……不允许表中的一行数据存储在不同页上……表中一行大小不能超过 8060B。」（ch03 §3.1.5）

> 「char[(n)] 按固定长度存储字符串……若输入的数据不足 nB，则补足后存储；varchar……存储空间大小为输入数据字节的实际长度+2B。」（ch04 §4.1.2）

> 「IDENTITY——指定列为一个标识列，一个表中只能有一个 IDENTITY 标识列……该列值不能由用户更新，不能为空值，也不能绑定默认值和 DEFAULT 约束。」（ch04 §4.2.2）

> 「注意：修改的数据库的容量只能比最初分配给数据库的容量要大。」（ch03 §3.5.1）

## I 内化 + 记忆钩子

### 钩子一：CREATE 家族三兄弟（建/改/删 × 库/表）

| | 库 | 表 |
|---|---|---|
| 建 | CREATE DATABASE | CREATE TABLE |
| 改 | ALTER DATABASE | ALTER TABLE |
| 删 | DROP DATABASE | DROP TABLE |

2×3=6 条命令背全，"创建、修改、删除数据库的 SQL 命令"就是 ch03 练习原题。附加库是 CREATE DATABASE 的隐藏第四用法：`FOR ATTACH`。

### 钩子二：建库五件套 NAME/FILENAME/SIZE/MAXSIZE/FILEGROWTH

逻辑名、物理路径、初始量、天花板、长速——一个 filespec 括号内五件套，数据文件挂 `ON [PRIMARY]`，日志文件挂 `LOG ON`。默认增长速度：数据文件 **1MB**、日志文件 **10%**（"数据要个整数，日志按百分比飘"）。FILEGROWTH=0 = 不许长。

### 钩子三：文件三兄弟 mdf/ndf/ldf —— "主、次、账本"

- **m**df 主数据文件：有且只有一个，库的起点；
- **n**df 次要数据文件：0~n 个，可摊到多块盘；
- **l**df 事务日志：至少 1 个，记流水账，坏了能靠它恢复。
ldf 三条硬规矩：**不属于任何文件组**、**数据与日志不同文件**、**一个文件只属一个库**。

### 钩子四：页 8KB，行 8060B

8192 = 8060（数据）+132（系统）。行不许跨页 → 每行 ≤8060B。算空间题公式：`每页能装几行 = 8060 ÷ 行字节（向下取整）→ 页数 = 行数 ÷ 每页行数 → 空间 = 页数 × 8KB`。

### 钩子五：类型选型四判据 —— 定变？中英？大小？算不算？

1. **定变**（定长 or 变长）：长度固定的代码选 char；长短不一选 varchar（多付 2B 管理费换空间弹性）。
2. **中英**（ASCII or Unicode）：纯英文数字 char 系（上限 8000）；含汉字选 n 系（上限 4000，每字符双倍空间）。
3. **大小**（数值范围）：tinyint 1B/0~255 → smallint 2B → int 4B → bigint 8B，范围翻着长（2^8 → 2^15 → 2^31 → 2^63）。
4. **算不算**（要不要做算术）：**不做算术的数字串永远选 char**——学号、电话、身份证。要做精确小数算术选 decimal(p,s)（p 总位数含小数位、s 小数位，p≤38）；金额选 money（4 位小数）；科学计算才碰 float/real（近似值，不确定精度）；开关量选 bit（只认 0/1/NULL，塞别的按 1 存；≤8 个 bit 字段挤 1B）。时间：要日期+时间且范围大选 datetime（1753~9999）；精确到分、1900~2079 够用选 smalldatetime。

### 钩子六：ALTER TABLE 三板斧 —— 改、加、删

- 改列：`ALTER COLUMN 列 新类型`（只能一列一列改，不能改列名）
- 加列：`ADD 列 类型`（可加多个）
- 删列：`DROP COLUMN 列`
配套记忆：ALTER DATABASE 是另一套——`ADD FILE / ADD LOG FILE / REMOVE FILE / MODIFY FILE / MODIFY NAME=`。**MODIFY FILE 只能改大不能改小**，改小要找 DBCC SHRINK（收缩是另一门课的事，记住"改大用 MODIFY，改小用 SHRINK"即可）。

### 钩子七：IDENTITY 自动手 —— 一表一个、不喂饭、不许改

`IDENTITY(种子,增量)`，默认 (1,1)；用户不许插值、不许更新、不许绑默认值；常和 PRIMARY KEY 搭档（一个出号，一个管唯一）。

### 钩子八：系统数据库四兄弟 —— master 管家、model 模板、tempdb 草稿、msdb 闹钟

- **master**：全系统的户口本，坏了服务器瘫，动过就备份；
- **model**：新建库的模板，改它=改未来所有新库；
- **tempdb**：草稿纸，重启清空，别存真数据；
- **msdb**：定时任务/报警的调度台。
不写 USE 时默认连 master——在管家头上动土最危险，所以开口第一句先 `USE 目标库`。

## A1 书中例题

**例 A1-1 建 jifei 数据库**（ch03 §3.2.2 例 3.2，表 3-3）
问题：建库 jifei——主数据文件初始 10MB、最大 100MB、每次长 2MB，日志文件初始 2MB、最大 50MB、每次长 20%。
规则：钩子二五件套 + ON/LOG ON 分区。
结论：
```sql
CREATE DATABASE jifei
ON PRIMARY
( NAME = jifei_data,
  FILENAME = 'D:\jifeiDB\jifei_data.mdf',
  SIZE = 10MB, MAXSIZE = 100MB, FILEGROWTH = 2MB )
LOG ON
( NAME = jifei_log,
  FILENAME = 'D:\jifeiDB\jifei_log.ldf',
  SIZE = 2MB, MAXSIZE = 50MB, FILEGROWTH = 20% )
GO
```

**例 A1-2 建"专业"表带主键**（ch04 §4.2.2 例 4.2）
问题：专业表——专业代码 char(4) 主键（约束名 pk_zydm）、专业名称 varchar(20) 非空、系部代码 char(2)。
规则：钩子一 + 列定义三要素（类型、长度、空不空）。
结论：
```sql
USE student
GO
CREATE TABLE 专业
( 专业代码 char(4) CONSTRAINT pk_zydm PRIMARY KEY,
  专业名称 varchar(20) NOT NULL,
  系部代码 char(2) )
GO
```

**例 A1-3 建"学生"表带外键**（ch04 §4.2.2 例 4.3）
问题：学生表——学号 char(12) 主键、姓名 char(8)、性别 char(2)、出生日期/入学时间 datetime、班级代码 char(9) 外键引用班级表。
规则：外键写法 `CONSTRAINT 约束名 REFERENCES 主表(主列)`，被引用列必须先有主键。
结论：
```sql
CREATE TABLE 学生
( 学号 char(12) CONSTRAINT pk_xh PRIMARY KEY,
  姓名 char(8), 性别 char(2),
  出生日期 datetime, 入学时间 datetime,
  班级代码 char(9) CONSTRAINT fk_bjdm REFERENCES 班级(班级代码),
  系部代码 char(2), 专业代码 char(4) )
GO
```

**例 A1-4 ALTER TABLE 三连**（ch04 §4.3.2 例 4.4~4.6）
问题：给"学生"表加"家庭住址 varchar(40)"→ 改成 varchar(50) → 删除该列。
规则：钩子六三板斧。
结论：
```sql
ALTER TABLE 学生 ADD 家庭住址 varchar(40)
ALTER TABLE 学生 ALTER COLUMN 家庭住址 varchar(50)
ALTER TABLE 学生 DROP COLUMN 家庭住址
```

## A2 触发题型 ★

**题型 1：给业务场景写建表语句**
- 信号词：「设计一张××表」「根据表结构写出 CREATE TABLE 语句」「用 T-SQL 创建××表，要求……主键/外键/不为空」
- 解法：钩子五选类型 → 钩子六/例 A1-2、A1-3 排骨架。典型题：计费系统上机卡表（上机号 char(13) 主键、班级代码 char(10) 外键、上机密码 varchar(30)、余额 money、备注 varchar(50)）。

**题型 2：给字段选数据类型（说理由）**
- 信号词：「下列字段最适合的数据类型是」「为××列选择合适的数据类型并说明理由」「13 位学号应定义为什么类型」
- 解法：四判据过一遍。陷阱预置：13 位学号选 char(13) 不是 int；"性别"char(2)/nchar(1)；"是否通过"bit；"余额"money 不是 float。

**题型 3：ALTER 改表/改库**
- 信号词：「在××表中增加一列」「将××列的数据类型改为」「删除××列」「为数据库增加一个数据文件/日志文件」
- 解法：表用三板斧（ADD/ALTER COLUMN/DROP COLUMN），库用 ADD FILE … TO FILEGROUP / ADD LOG FILE / REMOVE FILE。

**题型 4：数据库文件/存储计算**
- 信号词：「主数据文件的扩展名是」「每个数据库至少包含……」「某表 20000 行、每行 5000B，约需多少存储空间」「一行数据最大多少字节」
- 解法：mdf/ndf/ldf 钩子三 + 页 8060B 公式（钩子四）。20000 行×5000B：每页 1 行 → 20000 页 → 约 156MB，浪费约 58MB。

**题型 5：判断/纠错题**
- 信号词：「下列说法错误的是」「改错：……」
- 高频坑：①"日志文件可以放入文件组"（错，永不入组）；②"一个数据库可有多个主数据文件"（错，只能一个 .mdf）；③"IDENTITY 列可以手工插入值"（错）；④"ALTER DATABASE MODIFY FILE 可缩小容量"（错，只能大）；⑤"NULL 等于 0 或空格"（错）；⑥"bit 字段输入 2 会报错"（错，按 1 存）。

## E 考场步骤 ★

**写 DDL 的填空式模板**（拿到建表/建库题先默写骨架再填空）：

```
第一步 定骨架：
  建库 → CREATE DATABASE 库名 ON PRIMARY(...) LOG ON(...)
  建表 → CREATE TABLE 表名( 列1定义, 列2定义, ... )
第二步 填列（建表）：每列按"列名 类型(长度) [NOT NULL] [约束]"四格填
第三步 填文件（建库）：每个文件括号内五件套 NAME/FILENAME/SIZE/MAXSIZE/FILEGROWTH
第四步 查漏：有主键吗？外键引用的列在主表里是主键吗？汉字列用 n 系了吗？
第五步 收尾：语句间用英文逗号，最后 GO
```

**判停条件**（满足即停，别再画蛇添足）：
- 题目只要求"创建表"→ 不必写 INSERT 测试数据（那是 D3/D4 的事）；
- 题目给全长度和空否 → 照抄，不自行"优化"类型；
- 题目没给约束名 → 可以省 CONSTRAINT 名（系统自动命名），写了也不加分不扣分；
- 题目没给路径/SIZE → 建库题写最小骨架 `CREATE DATABASE 库名` 即可，缺省项有默认值。

## B 边界 ★

**常见失分点：**

1. **数字串选数值型**：学号/电话/邮编/身份证选 char，选 int/bigint 直接丢分——不做算术、可能有前导零、等值匹配为主。钩子五判据 4。
2. **char/varchar 反着选**：定长代码用 varchar（白付 2B）；长度波动大的用 char（补空格浪费且比较时受尾部空格干扰）。char 查询快、varchar 省空间，理由要能说出来。
3. **NOT NULL 别漏也别滥**：题目标"允许为空"就不写 NOT NULL（默认可空）；主键列天然 NOT NULL 不必重复写。漏写非空约束是建表题最常见扣分。
4. **decimal(p,s) 参数写反**：p 是总位数（含小数位），s 是小数位；decimal(6,2) = 整数 4 位 + 小数 2 位。写成 decimal(2,6) 直接错。
5. **金额用 float**：float 是近似值，金额必须 money 或 decimal。
6. **隐式转换坑**：char 列与 int 比较、datetime 与字符串运算会发生隐式转换，日期字符串必须用单引号（`'2014-09-01'`）；字符数据输入一律加英文单引号。
7. **行超 8060B**：一行各列长度之和超 8060B（text/image 等大对象除外）插入失败——建超宽表前先算账。
8. **IDENTITY 列手工塞值**：INSERT 显式给 IDENTITY 列赋值报错（除非 SET IDENTITY_INSERT ON，考试不要求掌握开关，记住"默认不许塞"即可）。
9. **MODIFY FILE 改小**：容量只能调大；缩小是 DBCC SHRINKDATABASE/SHRINKFILE 的活。
10. **删正在用的库**：数据库被连接使用时 DROP 失败；系统数据库永远不能删。

**与兄弟单元的边界混淆表：**

| 易混点 | 归属 | 区分口诀 |
|---|---|---|
| PRIMARY KEY / FOREIGN KEY / UNIQUE / CHECK / DEFAULT 约束的**语义与完整性分类** | D1 完整性 | D2 只管"约束写在建表语句哪个位置、语法长什么样"；为什么这样设计、实体/参照/用户定义完整性归类 → 找 D1 |
| SELECT / INSERT / UPDATE / DELETE | D3 查询 | 见到"查数据、加记录、改记录"→ D3；D2 的 INSERT 仅出现在"IDENTITY 列不许手工插值"这条规则里 |
| 视图、索引、存储过程、触发器的创建语法 | D5/D7 | ch03§3.1.1 只做对象名词铺垫；CREATE VIEW/INDEX/PROC 的语法不归 D2 |
| 数据库备份/恢复/收缩/分离附加细节 | 维护单元 | D2 只保留两个考点：日志文件用于恢复；附加 = CREATE DATABASE … FOR ATTACH |
| "每个表都要有主键" | 常识 | 不占考点名额，属于常识；考试真正会考的是**怎么写**主键约束，不是要不要有 |

---

**审计信息**：候选 35 → 通过 31（V1✓≥2 小节佐证，V2✓4 道书外新题全部解出，V3'✓31 条均对应可失分考点）→ 淘汰 4（存储过程前缀、恢复模式三选项、DBCC 收缩细节、GUI 操作步骤，理由见 verified.md）。审计日期：2026-09-13
