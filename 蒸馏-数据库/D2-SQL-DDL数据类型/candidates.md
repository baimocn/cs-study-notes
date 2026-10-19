# D2 候选池 — SQL DDL 与数据类型

来源：ch03《数据库的基本操作》、ch04《表的基本操作》。
每条注出处小节。分类：框架 F / 原则规则 R / 案例 C / 反例 X / 术语 T。

## 一、框架类

- **F1. 数据库 = 数据文件 + 事务日志文件；文件三类型 mdf/ndf/ldf**
  主数据文件（.mdf）每库有且只有一个，存数据和启动信息；次要数据文件（.ndf）0~n 个；事务日志文件（.ldf）至少一个可多个，记录所有操作事件，可用于恢复。〔ch03 3.1.3〕
- **F2. CREATE DATABASE 骨架**
  `CREATE DATABASE 库名 ON [PRIMARY](NAME=…,FILENAME='路径',SIZE=…,MAXSIZE=…,FILEGROWTH=…)[,…n] [LOG ON(…)] [FOR ATTACH]`。语法符号约定：[]可省、{}必选、|二选一、[,…n]可重复。〔ch03 3.2.2 / 3.7〕
- **F3. CREATE TABLE 骨架**
  `CREATE TABLE 表名(列名 数据类型 [NULL|NOT NULL] [IDENTITY(seed,increment)] [列约束][,…n])`。表名≤128字符，临时表≤116。〔ch04 4.2.2〕
- **F4. ALTER TABLE 三动作**
  `ALTER COLUMN 改列定义` / `ADD 增列或约束` / `DROP COLUMN 删列`。〔ch04 4.3.2〕
- **F5. DDL 动词矩阵：建/改/删 × 库/表 两级**
  CREATE DATABASE、ALTER DATABASE、DROP DATABASE；CREATE TABLE、ALTER TABLE、DROP TABLE。〔ch03 3.2/3.5/3.8，ch04 4.2/4.3/4.4 综合归纳〕

## 二、原则规则类

- **R1. 文件与文件组硬规则**
  ①一个文件/文件组只能被一个数据库使用；②一个文件只存在于一个文件组；③数据文件与日志文件不能共存于同一文件或文件组；④日志文件不属于任何文件组。〔ch03 3.1.4，另 3.2.1 亦重述"日志文件不属于任何文件组"——双重出处〕
- **R2. 页与 8060B 上限**
  存储分配单位是页（Page），一页 8KB=8192B，其中 8060B 存数据、132B 存系统信息；行不能跨页存储（varchar(max)/text/image 等除外），故一行各列之和≤8060B。〔ch03 3.1.5〕
- **R3. char 定长 vs varchar 变长**
  char(n)：n 为 1~8000，不足 nB 补足存储，超过截断；varchar(n|max)：按实际长度+2B 存储。char 查询快，长度不固定或有空值时用 varchar。n 省略默认 1。〔ch04 4.1.2 字符型〕
- **R4. unicode 家族容量减半**
  nchar/nvarchar/ntext 用法对应 char/varchar/text，但 n 上限 1~4000（char 系 1~8000），因 unicode 每字符占空间更大。〔ch04 4.1.2 unicode〕
- **R5. 整数四类型：8-4-2-1 字节链**
  bigint（-2^63~2^63-1，8B）、int（-2^31~2^31-1，4B）、smallint（-2^15~2^15-1，2B）、tinyint（0~255，1B）。〔ch04 4.1.2 整数型〕
- **R6. decimal(p,s) 参数语义**
  p=精度（总位数，不含小数点，最大 38），s=小数位数（0~p，默认 0）；numeric 与 decimal 用法相同。〔ch04 4.1.2 精确数值型〕
- **R7. float/real 是近似值**
  float(n)，n 为 1~53；real 4B。近似数值"不能确定所输出的数值精确度"；需精确定小数用 decimal。〔ch04 4.1.2 近似数值〕
- **R8. money/smallmoney 精确到万分之一**
  money 8B（约 ±922 万亿），smallmoney 4B（±214748.3647），均精确到货币单位的万分之一（4 位小数）。〔ch04 4.1.2 货币数据〕
- **R9. bit 类型三值特性**
  bit 只取 1、0 或 NULL；输入 0/1 之外的任何值系统都按 1 处理；表中 ≤8 个 bit 字段共用 1B 存储。〔ch04 4.1.2 位类型〕
- **R10. datetime vs smalldatetime**
  datetime：1753-1-1 ~ 9999-12-31，精确到 3.33ms（23:59:59.997）；smalldatetime：1900-1-1 ~ 2079-6-6，精确到分。〔ch04 4.1.2 日期时间〕
- **R11. IDENTITY 标识列规则**
  一表只能有一个 IDENTITY 列；系统自动赋唯一递增值（seed 默认 1，increment 默认 1）；该列不能由用户更新、不能为空、不能绑定默认值/DEFAULT 约束；常与 PRIMARY KEY 同用。〔ch04 4.2.2〕
- **R12. FILEGROWTH 默认值与 0 值语义**
  FILEGROWTH 可按 MB/KB/GB/TB/%，须整数不能含小数；=0 表示文件不增长；未指定时数据文件默认增长 1MB、日志文件默认 10%。〔ch03 3.2.2 表 3-2〕
- **R13. 容量修改只能大不能小**
  `ALTER DATABASE … MODIFY FILE` 修改的容量只能比最初分配的大；要缩小用 DBCC SHRINKDATABASE / SHRINKFILE。收缩整个库不能小于创建时初始大小，收缩单个文件可以小于初始大小，但任何收缩不能小于现存数据所占空间。〔ch03 3.5.1 / 3.5.2〕
- **R14. 系统数据库四兄弟**
  master（系统核心信息，损坏则服务器瘫痪，改动后应及时备份）、model（模板库，改它影响之后新建的所有库）、tempdb（临时对象，重启即清空，不能当最终存放处）、msdb（任务调度/报警）。〔ch03 3.1.2〕
- **R15. NULL 语义**
  NULL 既不是 0 也不是空格，表示"尚未输入或明确插入 NULL"；NOT NULL 列插入/修改时必须给值。〔ch04 4.2.2〕
- **R16. 删除库/表不可逆 + 删库限制**
  DROP DATABASE / DROP TABLE 删除后数据与定义一并永久删除；正在被使用的数据库无法删除；不能删除系统数据库；仅 dbo 和 sa 可删库。〔ch03 3.8，ch04 4.4〕

## 三、案例类

- **C1. 例 3.2 建 jifei 数据库**
  ON PRIMARY(NAME=jifei_Data, FILENAME='D:\jifeiDB\jifei_Data.mdf', SIZE=10MB, MAXSIZE=100MB, FILEGROWTH=2MB) LOG ON(NAME=jifei_log, …, FILEGROWTH=20%)。〔ch03 3.2.2 例 3.2〕
- **C2. 例 4.1~4.3 建系部/专业/学生表**
  系部：char(2) NOT NULL + varchar(30) + char(8)；专业：加 `CONSTRAINT pk_zydm PRIMARY KEY`；学生：加 `CONSTRAINT fk_bjdm REFERENCES 班级(班级代码)` 外键（被引用列须先为主键）。〔ch04 4.2.2 例 4.1/4.2/4.3〕
- **C3. 例 4.4~4.6 ALTER TABLE 三连**
  ADD 家庭住址 varchar(40) → ALTER COLUMN 家庭住址 varchar(50) → DROP COLUMN 家庭住址。〔ch04 4.3.2〕
- **C4. 例 3.14~3.15 ALTER DATABASE 加文件**
  ADD FILE … TO FILEGROUP / ADD LOG FILE；删除用 REMOVE FILE / REMOVE FILEGROUP。〔ch03 3.5.4〕
- **C5. 计费系统建表群（类型选型活教材）**
  上机卡：上机号 char(13) 主键、余额 money、密码 varchar(30)；上机记录：三个 datetime + 上机状态 bit；课程注册：注册号 bigint IDENTITY(01000000,1) NOT FOR REPLICATION、成绩 tinyint、学期 tinyint。〔ch04 4.7.2〕

## 四、反例类

- **X1. 定长/变长选反**
  用 char(30) 存最长 10 字、普遍 5 字的备注 → 大量补空格浪费；反之用 varchar 存固定 2 位代码 → 多 2B 开销且无收益。〔ch04 4.1.2〕
- **X2. 数字型学号/身份证误用数值类型**
  学号 char(12)、身份证号定长数字串应选 char——不参与算术、可能含前导零、常做等值匹配；用 int 丢前导零且范围浪费。〔ch04 4.7.1/4.7.2 各表学号均 char(12) 可佐证〕
- **X3. bit 塞入 2**
  bit 字段输入 2 → 系统按 1 存，逻辑判断失真。〔ch04 4.1.2〕
- **X4. 行超 8060B**
  一行各列之和超过 8060B 时插入失败（大对象类型除外）。〔ch03 3.1.5〕

## 五、术语类

- **T1. 数据类型的作用定义**
  数据类型决定数据的存储格式、存储长度、数据精度和小数位数；建表时每列必须确定数据类型，即确定取值范围。〔ch04 4.1.2 开头〕
- **T2. 表与关系模型对应**
  关系→表、属性→列、元组→行/记录、关系模式→表定义、主键→约束。〔ch04 4.1.1 表 4-2〕
- **T3. 存储过程前缀** sp_ 系统 / xp_ 扩展 / up_ 用户。〔ch03 3.1.1〕
- **T4. 数据库默认库陷阱**
  不指定连接库时默认连 master，对 master 误操作后果严重，故应 USE 切换。〔ch03 3.4〕
- **T5. 分离与附加**
  分离=脱离服务器实例但文件保留在磁盘；附加=CREATE DATABASE … FOR ATTACH 把既有 mdf 挂回（或挂到）服务器。〔ch03 3.6/3.7〕
