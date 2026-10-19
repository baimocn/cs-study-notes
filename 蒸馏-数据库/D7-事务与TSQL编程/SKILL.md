---
name: D7-事务与TSQL编程
description: 自考《数据库原理与技术(SQL Server 2012)》D7 单元：T-SQL 编程与事务、存储过程与触发器。覆盖 ch09 批处理/GO/两类注释、变量 DECLARE/SET/SELECT 赋值差异、流程控制；事务 ACID 四属性与 BEGIN TRAN/COMMIT/ROLLBACK 对偶、SAVE TRAN 保存点、@@ERROR/@@TRANCOUNT、锁与死锁；ch10 存储过程五类型与创建/执行/修改/删除四动词、EXEC 与 OUTPUT 参数、触发器"自动触发 vs 显式调用"根本区别、AFTER/INSTEAD OF、inserted/deleted 虚表、嵌套与递归、DDL 触发器。面向简答四连（事务四性起因于什么）与 CREATE PROC/CREATE TRIGGER 骨架填空题，含四格填空法、触发器三步法、失分点辨析与 OCR 修复记录。
source_book: 数据库原理与技术（SQL Server 2012）
source_chapter: ch09-SQLServer程序设计 + ch10-存储过程与触发器
---

# D7 事务与 T-SQL 编程

## R 原文根

- ch09.2.1：事务是 SQL Server 中的执行单元，由一系列 T-SQL 语句组成，要么成功完成所有操作，要么失败并将所做的一切复原。
- ch09.2.1 原文："事务有四个原则，统称 ACID 原则"，四条逐字展开见 A2。
- ch10 章首原文：存储过程由一组预先编辑好的 SQL 语句组成，放在服务器上由用户指定名称执行；触发器是一种特殊类型的存储过程，不是由用户直接调用的，而是当用户对数据库进行操作和管理时自动激发执行。
- OCR 工伤说明：`存储诸过程`/`存诸过程`→`存储过程`（ch10 专题）已修，本文引文均按修复后转写。

## I 内容骨架

### 1. 批处理 / GO / 注释（ch09.1）

- 批处理 = 一条或多条 T-SQL 语句的集合，一次性发送，编译成一个执行计划，计划内语句每次执行一条。
- GO = 批处理结束标记；它**不是 T-SQL 语句**，是客户端实用程序（如 SSMS 查询窗口）识别的指令；服务器收到的批中不含 GO；GO 行上只能放注释不能放其他语句。
- 差错规律：批中有**语法错误**（如引用不存在的对象）→整批不能编译；只有**执行错误**（如违反约束）→只终止出错处到本批末尾，前面的语句和其他批不受影响。
- 六条限制（判断题高发）：①CREATE DEFAULT/PROCEDURE/RULE/TRIGGER/VIEW 不能与其他语句同批；②删对象后不能同批再引用它；③变量不能跨批引用；④规则/默认值绑定到列后不能立即同批用；⑤CHECK 约束定义后不能立即同批用；⑥改列名后不能立即同批引新名。
- 脚本 = 以文件存储的按顺序提交的批处理序列；无 GO 则整体当单个批执行。
- 注释两类：行内 `--注释`（双连字符至行尾）；块注释 `/*注释*/`（可多行、可嵌代码中）。陷阱：整个注释必须包含在一个批处理中，**多行注释不能跨越批处理**。

### 2. 变量（ch09.3）

- 全局变量 @@开头：系统定义维护，共 32 个，只能读不能写，本质是**系统函数**。常考：@@ERROR（最后一条语句错误码）、@@ROWCOUNT（上一语句影响行数）、@@TRANCOUNT（活动事务数）、@@IDENTITY、@@VERSION。
- 局部变量 @开头：用户定义，作用域=声明处到所在批处理/可编程对象结束，批一结束自动消亡；不能声明为 text/ntext/image。
- 赋值规则（判断题冠军）：**SELECT 一条语句可赋多个变量；SET 一条语句只能赋一个变量**；SELECT 返回多个值时变量取最后一个；复合赋值 SET @a+=1。
- 输出通道：PRINT 走"消息"窗格，SELECT 走"结果"窗格。

### 3. 流程控制（ch09.4）

- BEGIN...END 语句块可嵌套；IF...ELSE 分支（逻辑表达式含 SELECT 时必须加圆括号）。
- CASE 两格式（简单 CASE 比 WHEN 值 / 搜索 CASE 测逻辑表达式），均无 ELSE 时返回 NULL。
- WHILE 循环：BREAK 退出（嵌套中内层 BREAK 转到外一层继续）、CONTINUE 跳回 WHILE 行；可嵌套。
- WAITFOR：DELAY 间隔后 / TIME 到点执行；HH:MM:SS 格式，不允许日期部分。

## A1 应用例题（书中原例）

### ch09 例 9.3 显式事务骨架

```
BEGIN TRANSACTION
  INSERT 班级 VALUES (...) ; SAVE TRAN ST          -- 保存点
  UPDATE 教师 SET 职称='讲师' WHERE ... ; DELETE FROM 教师 WHERE ...
  SAVE TRAN ST                                     -- 保存点重名：旧 ST 失效
  INSERT 教师 VALUES (...)
  IF @@ERROR<>0 ROLLBACK TRAN ST  ELSE  COMMIT TRAN
```

- 同名保存点重用时，ROLLBACK 只认**第二个**，第一个被忽略；没设保存点则回滚到事务定义起始位置。

### ch10 存储过程骨架（例 10.2 / 案例·单科成绩分析）

```
CREATE PROCEDURE ST_PRO_BJ AS
  SELECT 班级名称 FROM 班级,系部 WHERE 系部.系部代码=班级.系部代码 AND 系部.系部名称='计算机系'
EXEC ST_PRO_BJ
```

- 带输出参数：CREATE PROCEDURE 单科成绩分析 @KECHENGMING varchar(20), @AVGCHENGJI tinyint OUTPUT, ... AS SELECT @AVGCHENGJI=AVG(成绩),... FROM 课程注册 WHERE ...；执行 EXEC 单科成绩分析 @KECHENGMING, @AVGCHENGJI1 OUTPUT, ...（形参、实参都加 OUTPUT）。

### ch10 触发器四例骨架

- 例 10.17 INSERT 后触发（FOR INSERT 默认即 AFTER）：`CREATE TRIGGER ins_jxjh ON 教学计划 FOR INSERT AS INSERT 教师任课(...) SELECT ...,30 FROM inserted`。
- 例 10.18 UPDATE 后触发+IF UPDATE(列)：`CREATE TRIGGER up_jsrk ON 教师任课 FOR UPDATE AS IF UPDATE(专业学级) BEGIN PRINT('不能修改专业学级信息！') ROLLBACK TRANSACTION END`。
- 例 10.19 UPDATE 替代触发：`CREATE TRIGGER up_jsrk ON 教师任课 INSTEAD OF UPDATE AS SELECT '不能修改该表信息！'`。
- 例 10.20 DELETE 后触发：`CREATE TRIGGER del_xs ON 学生 FOR DELETE AS DELETE 课程注册 WHERE 学号 IN (SELECT 学号 FROM DELETED)`。
- 例 10.23 DDL 触发器：`CREATE TRIGGER SafetyXS ON DATABASE FOR DROP_TABLE,ALTER_TABLE AS PRINT('禁止删除或修改当前数据库中的表！') ROLLBACK TRANSACTION`。

## A2 触发题型★

### 简答考区 1：事务哪四性、起因于什么（ACID 四连必考）

- 答题先给定义：事务 = SQL Server 中的执行单元，由一系列 T-SQL 语句组成，要么全部成功要么全部复原；提出目的 = 防止多用户并发访问同一数据时造成的数据异常。
- ① 原子性 atomicity：事务是原子的，要么完成所有操作，要么退出所有操作；某语句失败则作为事务一部分的所有语句都不会运行。（钩：全做或全不做；起因：多操作必须捆绑成不可分割整体。）
- ② 一致性 consistency：事务完成或失败时，数据库处于一致状态；事务引发的状态变化是一致的。（钩：账目不坏；起因：状态变迁必须守恒。）
- ③ 隔离性 isolation：事务是独立的，不与数据库的其他事务交互或冲突。（钩：排队不串；起因：并发访问的相互控制。）
- ④ 持久性 durability：事务成功完成后对数据的改变是永久的；突然掉电或服务器崩溃也能保证事务在服务器重启后仍完整。（钩：停电不丢；起因：须扛住系统故障。）

### 简答考区 2：存储过程 vs 触发器（必考）

- 同源句：触发器是一种事件驱动的特殊类型的存储过程，同为预编译存于数据库的 SQL 语句集。
- 差异 1 调用方式：存储过程由用户/程序用名称或 EXEC 显式调用（请饭：点菜才上菜）；触发器捆绑在基表或视图上，当用户对表中数据进行修改时自动执行（保安自动拦）。
- 差异 2 参数：存储过程接收输入参数并以输出参数返回多个值；触发器不可能通过名称被直接调用，更不允许使用参数。
- 差异 3 依附：存储过程是独立的数据库对象；触发器与表紧密相连，可以看作表定义的一部分。
- 追加加分：触发器事件三要素 = 事件 / 条件 / 动作；触发器可评估数据修改前后的状态并按差异采取措施。

### 简答考区 3（次热点清单）

- 存储过程优点三条：①接收输入参数并以输出参数返回多个值；②包含执行数据库操作（包括调用其他过程）的编程语句；③返回状态值表明成功或失败。外加：预编译代码存高速缓存→执行效率高。
- 触发器优点五条：自动执行；级联操作（一个表触发、可操作多个相关表）；比 CHECK 更复杂（CHECK 不能引用其他表列，触发器可以）；可评估修改前后状态；一个表可同时存在多个不同操作的触发器。
- 事务分类：显式事务（用户 BEGIN TRANSACTION 定义）/ 隐式事务（系统提供，一条 INSERT/DELETE/UPDATE/SELECT/CREATE/ALTER/DROP/TRUNCATE TABLE/GRANT/REVOKE 等语句即一个事务——GRANT/REVOKE 仅在清单点名，机制归 D8）。

## E 考场步骤

### 写存储过程题——四格填空法

1. 第一格 CREATE：`CREATE PROCEDURE 过程名 [@参数 数据类型 [=[默认值]] [OUTPUT]]`。
2. 第二格 参数收口：输入参数直接列；输出参数形参加 OUTPUT，执行时实参也要加 OUTPUT。
3. 第三格 AS 过渡：`AS`（可再 BEGIN...END 包体）。
4. 第四格 主体+执行：业务句照写；执行 `EXEC 过程名 实参 [OUTPUT]`。特判：过程是批处理第一条语句时 EXEC 可省略，直接写过程名。
- 可选项：WITH RECOMPILE（每次重编译）、WITH ENCRYPTION（加密文本）。
- 四动词配套：建 CREATE / 改 ALTER / 删 DROP（可一次删多个、可删 ;number 组）/ 调 EXEC；查文本 sp_helptext、一般信息 sp_help、相关性 sp_depends。

### 触发器题——三步法

1. 判表：数据改动在哪个表，`ON` 谁写谁。
2. 判句："事件成功后补动作" → FOR/AFTER 后触发（只能建在表上不能在视图上，每个操作可建多个）；"取消原语句以动作替代" → INSTEAD OF 替代触发（表和视图都可建，每个操作只能一个）。
3. 写虚表引用：INSERT 题读 **inserted**（新行副本、触发器表与之有相同记录）；DELETE 题读 **DELETED**（触发器表已无该记录、deleted 独存）；UPDATE=先删旧后插新→旧值进 deleted、新值进 inserted；限定列则用 `IF UPDATE(列)`（不能用于删除操作）。
4. 收口：违约处理常配 `PRINT 提示 + ROLLBACK TRANSACTION`。
5. 旁项检查：CREATE TRIGGER 必须是批处理中第一条语句；不能建在临时表/系统表上。

### 撞 B 边界时的辨析题速断

- "触发器可以用 EXEC 调用"——**错**（见 B 第 1 条）；"多行注释跨 GO"——**错**（见骨架第 1 节）；提示后细节走 B 边界，数字记不全时先保 ACID 四钩。

## B 边界★失分点

1. EXEC 调用触发器是**伪命题**：教材 10.2.2 原文"不可能通过名称被直接调用，更不允许使用参数"。钩子复述：请饭（存储过程）上菜要 EXEC 点名，保安（触发器）拦人绝不点名。
2. ROLLBACK 后 @@TRANCOUNT 拆两半说：回滚到事务开始点→**减 1**；只回滚到保存点→**不变**（释放从保存点起的修改、之前的仍有效）。
3. @@ERROR 时序：只记**最后一条**执行语句的错误码（0=无错）；判错必须紧跟出错语句，隔句后也被清 0。
4. COMMIT WORK vs COMMIT TRANSACTION：前者不带参数。
5. TRUNCATE TABLE 不记日志：不触发 DELETE 触发器；触发器动作中也不能含 TRUNCATE TABLE。
6. 数字别对调：**嵌套**默认允许、上限 32 层、不允许迭代调用自己；**递归**（直接/间接）默认禁用、最多 16 层、第 17 层直接回滚。
7. 权限细节：表所有者有创建触发器的默认权限，且不能转给其他用户。
- 混淆表（vs D8 安全管理）：
  | 混淆点 | D7 答 | D8 答 |
  |---|---|---|
  | GRANT/REVOKE | 只是隐式事务清单成员（一条 GRANT 即一事务） | 授权/回收主角 |
  | 保护目标 | 操作不坏（全改或全不改） | 人不配看（按身份定资格） |
  | 回退/收回 | ROLLBACK 撤销本次改动 | REVOKE 收回长期资格 |
- 约束优先级：维护完整性时**外键约束优先于触发器**——例 10.20 需改 INSTEAD OF DELETE 去化解（教材教学做法：先 DROP 再 ADD fk_kczcxh）。
- 锁件三套（隔离性追问自备）：粒度行/页/扩展盘区/表/数据库（小粒度高并发但开销大，升级按 2% 标准）；共享 S 锁（SELECT、可多共存）、排他 X 锁（唯一，INSERT/DELETE/UPDATE）、更新锁（UPDATE 两阶段升格）；死锁：预防=一次/顺序封锁、诊断=超时/等待图回路、解除=最小代价牺牲并恢复其已做修改。

## 数字钩子表

| 数字 | 归属 | 一句话 |
|---|---|---|
| 32 | 全局变量总数 | @@ 系统函数式全局变量共 32 个 |
| 32 / 16+17 | 嵌套 32 层 / 递归 16 层第 17 层回滚 | 默认：嵌套允许、递归禁用 |
| 32 | 事务名长度 | 字符不超过 32 个 |
| 128 | 局部变量名 | 最长 128 字符 |
| 2% | 锁升级标准 | 超页 2% 行升页锁、超表 2% 页升表锁 |

## 依赖与后续

- 前置 D6：函数语法归 D6，本单元只在"全局变量本质是系统函数"一句带过。
- 边界分工：D6 函数与查询语法 / D7 事务与两个语句包 / D8 权限与安全；GRANT、REVOKE 在 D7 只以隐式事务身份出现一句话。
- 自检三问：ACID 四钩了吗？请饭/保安对上号了吗？inserted/deleted 指认事件了吗？

## 审计信息

- 作者：单元工兵 D7；日期：2026-05。链路：candidates.md（12 候选）→ verified.md（12 通过 + 7 条淘汰/降权留痕）→ SKILL.md。
- OCR 坏字全清单（ch10 重灾区，逐条）：
  1. `存储诸过程`→`存储过程`（ch10 页眉横标与 10.1 综述标题，多处）；
  2. `存诸过程`→`存储过程`（10.1.2 远程存诸过程、10.1.3 执行/查看/删除存诸过程、10.1.5 建立存诸过程、10.1.6 扩展存诸过程、10.1.7 存诸过程、练习题 1，多处）；
  3. `创建一个查询存储诸过程`→`…存储过程`（10.1.7）；
  4. `查询存储诸过程`→`查询存储过程`（案例首行）；
  5. `SOL Server`/`SOLServer2012`→`SQL Server`（两章页眉反复）；
  6. `香询`→`查询`（ch09 图 9-1 题注"在香询窗口中执行批处理"）；
  7. `册删除`→`删除`（10.1.3"语句册删除存储过程"）；
  8. `弓引用`/`引I用`→`引用`（inserted/deleted 工作原理段多处）；
  9. `sp_setriggerorder`→`sp_settriggerorder`（10.2.4）；
  10. `sp_config`→`sp_configure`（10.2.4 嵌套设置段）；
  11. `RECOMPLE`→`RECOMPILE`（10.1.3/10.1.5 语法多处）；
  12. 例 10.23 触发器名 SafetyXS / 图内 safetySTUDENT 抖动——取 SafetyXS。
- 交接 D8：仅在"权限 vs 事务"边界发出 GRANT/REVOKE 信号，不展开机制。
