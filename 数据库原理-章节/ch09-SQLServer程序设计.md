# 第9章 SQLServer程序设计

SQL语言是操作关系数据库的通用标准语言，能进行数据定义、数据操纵、数据控制 等与数据库有关的全部功能，是一种非过程化的语言。不同数据库厂商的 提供的 DBMS SQL语言略有差别。Microsoft SQL Server 中使用的 SQL语言称为 T-SQL语言。应用程序 必须通过向服务器发送T-SQL语句才能实现与 SQL Server 的通信。 本章主要介绍基于T-SQL语言的编程基本控制语句及相关概念。

## 程序中的批处理、脚本、注释

### 9.1

有些任务不能由单独的 T-SQL语句完成，这时就要使用 SQL Server 的批处理、脚本、 存储过程、触发器等组织多条T-SQL语句来完成。本节主要介绍批处理、脚本等基本概念。

### 9.1.1

批处理 批处理是一条或多条 T-SQL 语句的集合，从应用程序一次性发送到 SQL Server 并由 SQL Server 编译成一个可执行单元，此单元称为执行计划。执行计划中的语句每次执行 一条。 建立批处理时，使用 GO 语句作为批处理的结束标记。GO 语句本身并不是 T-SQL语 句的组成部分，而是由各种 SQL Server 命令实用程序(如 SSMS 中的“查询”窗口)识别的 命令，它只是一个用于表示批处理结束的指令。当这些使用程序读取到GO语句时，会把

给服务器，不包含GO语句。 在一个GO语句行中不能包括其他 T-SQL语句，但可以使用注释文字。如果在一个批 处理中包含语法错误，如引用了一个并不存在的对象，则整个批处理就不能被成功地编译 和执行。如果一个批处理中不存在语法错误，但某句有执行错误，如违反了约束，则它仅 影响该语句的执行。即执行错误将终止从错误发生的地方到此批处理未端的批处理的执行， 而其后批处理的编译执行不受影响。 建立批处理时，应当注意以下几点： (1） CREATE DEFAULT、CREATE PROCEDURE、CREATE RULE、CREATE TRIGGER 及CREATEVIEW语句不能与其他语句组合使用，放在一个批处理中。 (2) 不能在删除一个对象之后，在同一批处理中再次引用这个对象。 (3) 不能在一个批处理中引用其他批处理中所定义的变量。 不能把规则和默认值绑定到表字段或用户自定义数据类型之后，立即在同一个批 (4) 处理中使用它们。 数据库原理与技术（SOL Server 2012） (5) 不能定义一个CHECK约束之后，立即在同一个批处理中使用该约束。 （6）不能在修改表中的一个字段名之后，立即在同一个批处理中引用新字段名。 如果一个批处理中的第一个语句是执行某个存储过程的EXECUTE语句,则EXECUTE 278 E关键字，EXECUTE 可以省写为EXEC。 【例9.1】 利用集成管理器的查询窗口执行两个批处理，用来显示系部表中的信息及 记录个数。代码如下： UsE student GO ‘系部表包含如下信息： PRINT ＊ FROM 系部 SELECT '系部表记录个数为：「 PRINT COUNT（*）FROM 系部 SELECT GO 例9.1中包含两个批处理，前者仅包含一个语句，后者包含四个语句，其中，PRINT 语句用于在消息页中显示char、varchar类型，或可自动转换为字符串类型的数据。运行结 果如图9-1 所示 SQLQuery1.sql -S...ministrator (55))*X USE student GO 日PRINT系部表包含如下信息： SELECT*FROM系部 PRINT系部表记录个数为： SELECT COUNT（*）FROM系部 GO

100 % 脂消息 系部代码 系主任 系部名称 计算机系 徐才智 01 张博 经济管理系 02 徐裕光 数学系 03 外语系 李溅波 04 SKY-20170310IRLVAdmini...student[00:00:00|5行 SP1)

图 9-1 在香询窗口中执行批处理

脚本

### 9.1.2

脚本是以文件存储的一系列SQL语句，即一系列按顺序提交的批处理 T-SQL 脚本中可以包含一个或多个批处理。GO 语句是批处理结束的标志。如果没有 GO语句，则将它作为单个批处理执行 脚本可以通过集成管理器建立查询窗口来执行，这也是建立、编辑和使用脚本的首选 环境。在查询窗口中，不仅可以新建、保存、打开、编辑脚本文件，还可以通过执行脚本 来查看脚本的运行结果，从而检验脚本内容是否正确。 注释

### 9.1.3

注释是指程序中用来说明程序内容的文字，它不能执行且不参与程序的编译。注释用 于语句代码的说明，或部分语句的暂时禁用。为程序加上注释不仅能增强程序的可读性， 而且有助于日后的管理和维护。在程序中使用注释是一个程序员良好的编程习惯。SQL Server 支持两种形式的注释语句。

### 1．行内注释

如果整行都是注释而并非所要执行的程序行，则该行可用行内注释。语法格式为： --注释语句 这种注释形式用来在一行内加以注释，可以与要执行的代码处在同一行，也可以另起 一行。从双连字符（--）开始到行尾均为注释。

### 2．块注释

如果所加的注释内容较长，则可使用块注释。语法格式为： /*注释语句*/ 这种注释形式用来对多行加以注释，可以与要执行的代码处在同一行，也可以另起一 行，甚至可以放在可执行代码内。对于多行注释，必须使用开始注释字符（/*）开始注释， 使用结束注释字符（*/）结束注释，“/*”和“*/”之间的全部内容都是注释部分。注意： 整个注释必须包含在一个批处理中，多行注释不能跨越批处理 注释语句举例。 【例9.2】

注释语句应用示例 块注释 UsE student GO SELECT ＊ FROM 学生 --行注释：检索所有学生的情况 GO

## 程序中的事务

### 9.2

事务是 SQL Server中的执行单元，它由一系列 T-SQL语句组成。这个执行单元要么成 功完成所有操作，要么就是失败，并将所做的一切复原。事务机制的提出与实施是为了防 279 止多用户访问同一数据时造成的数据异常。本节主要讨论 MS SQL Server 2012 中的事务 机制。

SQL Server 程序设计 数据库原理与技术（SOLServer2012）

## 事务概述

### 9.2.1

由于事务的执行机制，确保了数据能够正确地被访问，避免因多个数据操作的并发或 280 是在访问数据过程中受到其他操作的干扰而造成数据不完整。 事务有四个原则，统称ACID原则。 （1）原子性（atomicity）：事务是原子的，要么完成事务中的所有操作，要么退出所有 操作。如果某语句失败，则所有作为事务一部分的语句都不会运行。 （2）一致性（consistency）：在事务完成或失败时，要求数据库处于一致状态。由事务 引发的从一种状态到另一种状态的变化是一致的。 （3）隔离性（isolation）：事务是独立的，它不与数据库的其他事务交互或冲突。 （4）持久性（durability）：事务成功完成后，其对数据库中数据的改变是永久的，它无 须考虑对数据库进行过的任何操作。如果系统突然掉电或数据库服务器崩溃，可保证事务 在服务器重启后仍是完整的。 事务可分为两种类型：显式事务和隐式事务。系统提供的事务和用户定义的事务。 隐式事务是由系统提供的事务，是指在执行某些T-SQL语句时，一条语句就构成了一 个事务，这些语句包括： DROP CREATE DELETE ALTER TABLE FETCH GRANT OPEN INSERT SELECT REVOKE UPDATE TRUNCATE TABLE

例如，执行如下的创建表语句： test CREATE TABLE (11 char(6), 12 char(8), 13 varchar(20)) 这条语句本身就构成了一个事务，它要么执行成功，建立起包含有三列的表结构；要 么执行失败，没有建立 test表（比如第二列的定义误写为12 chars(8))，对数据库没有产生 任何影响。绝不会建立起只包含一列或两列的表结构。 在实际应用中，根据需要，也可以使用显式事务。由用户自行将需要形成一个执行单 T-SQL语言定义显式事务的方法是：用BEGIN 元的语句组定义为事务。使用 TRANSACTION 语句指定一个事务的开始，用COMMIT 或 ROLLBACK语句表明一个事 务的结束。注意：必须明确指定事务的结束，否则系统将把从事务开始到用户关闭连接之 间所有的操作都作为一个事务来处理

## 事务处理语句

### 9.2.2

事务处理语句包括 BEGIN TRANSACTION、COMMIT TRANSACTION、ROLLBACK TRANSACTION 和 SAVE TRANSACTION 语句。 （1）BEGIN TRANSACTION 语句。BEGIN TRANSACTION 语句为事务的开始。其语 法格式为: BEGIN TRANSACTION [transaction namel@tran name variable] [WITH MARK［'description']] 其中: transaction name 是事务的名称，必须遵循标识符规则，但字符不超过 32个。 _ name_variable 是用户定义的、含有效事务名称的变量，该变量类型必须是 Atran char、varchar、nchar 或 nvarchar。 WITHMARK指定在日志中标记事务。 description 是描述该标记的字符串。 TRANSACTION可以只取前四个字符（以下同）。 （2）COMMIT TRANSACTION 语句。COMMIT是事务提交语句，它使得自从事务开 始以来所执行的所有数据修改成为数据库的永久部分，也标志一个事务的结束。其语法格 式为: [transaction namel@tran name variable] COMMIT TRANSACTION 其中，参数 transaction name 和@tran name_variable 分别是事务名称和事务变量名。与 的执行使全局变量 语句相反，COMMIT TRANSACTION BEGIN TRANSACTION @@TRANCOUNT 的值减 1。 标志一个事务的结束也可以使用 COMIMIT WORK语句。其语法格式为: COMMIT[WORK] 它与 COMMIT TRANSACTION 语句的差别在于：COMMIT WORK 不带参数 （3）ROLLBACK TRANSACTION 语句。ROLLBACK TRANSACTION 语句是事务撤 销语句，它使得事务撤销到起点或指定的保存点处，它也标志一个事务的结束。其语法格 式为: ROLLBACK TRANSACTION [transaction namel@tran name variable Isavepoint namel@savepoint variable 其中: 参数 transaction name 和@tran name variable 分别是事务名称和事务变量名。

## savepoint_name 是保存点名。

@savepoint_variable 是含有保存点名称的变量名，它们可用 SAVE TRANSACTION 语句设置。 ROLLBACKTRANSACTION语句将撤销自事务的起点或某个保存点起一直到该撤销 语句之间所做的所有数据修改，并且释放由事务控制的资源。如果事务撤销到开始点，则 281 全局变量@@TRANCOUNT的值减1，而如果只撤销到指定保存点，则@@TRANCOUNT 的值不变 也可以使用ROLLBACK WORK语句进行事务撤销，ROLLBACK WORK将使事务撤

SQL Server 程序设计 数据库原理与技术（SOLServer2012） 销到开始点，并使全局变量@@TRANCOUNT的值减1。 （4）SAVE TRANSACTION语句。SAVETRANSACTION语句是保存点设置语句，用 于撤销事务时指定事务撤销过程中的停止点。其语法格式为： 282 SAVE TRANSACTION (savepoint namel@savepoint Variable} 【例9.3】 事务举例。代码如下： USE student go --自定义一个显式事务 --事务定义开始 BEGIN TRANSACTION 班级 (班级代码，班级名称，专业代码，系部代码) INSERT VALUES（'010202003＇，'01级会计专业班＇，＇0202＇，'02'） --设置事务回滚的保存点 ST SAVE TRAN 教师 SET 职称='讲师' 教师编号=＇100000000005＇ UPDATE WHERE 姓名 IS NULL 教师 WHERE DELETE 教师 FROM SELECT --设置事务回滚的保存点 TRAN ST SAVE 教师 INSERT (教师编号,姓名，性别，出生日期,学历,职务,职称,系部代码，专业) VALUES（'100000000005'，'李明’，'男'，08／05／65，'研究生'，'副书记'，'副教授' '02'，'经济管理') IF @@ERROR<>0 --事务执行出错，回撤操作，结束事务，释放资源 ROLLBACK TRAN ST ELSE --事务执行成功，提交结果，结束事务，释放资源 TRAN COMMIT go 一-检验自定义事务的执行情况 select * from 教师 select * from 班级 06 在该例中，BEGIN TRANSACTION 命令指示事务的开始，COMMIT TRAN 命令指示 事务的结束，SAVETRAN命令用来生成保存点，其中的 ST 是保存点的名称，ROLLBACK TRAN命令将恢复事务到事务起始点或保存点位置 例中使用全局变量@@ERROR 的值来判断自定义事务中的操作执行是否有错。

## @@ERROR的值不为O，说明有错

（第二条insert 语句执行时，添加的教师编号值与原数 据发生主键冲突，执行失败），则执行ROLLBACK TRAN 撤销事务中已完成的操作。没有 使用 SAVE TRAN 命令设置保存点时，事务将回撤到事务定义的起始位置，回复到事务执 行前的数据状态。如果在事务定义中设置了保存点，则事务撤回到指定的保存点处。该例 中有两个保存点，而且名称相同，ROLLBACK TRAN 命令使事务恢复到第二个保存点， 第一个保存点由于名称被重用，所以被忽略了。@@ERROR的值为O（将第二条 insert 语 句中添加的教师编号值改为“100000000015”），所有操作均成功执行，则执行C0MMIT TRAN 提交事务。 要注意的是，@@ERROR记录的是最后执行的那条 T-SQL语句的错误情况。上例中, 若出错的操作不是 f 判断的前一条语句而是其前面的某条，则@@ERROR 记录了出错操 作的错误号后，又会被后面的成功操作将其值置为0，从而不能撤销事务，所以在实际应 用时需要考虑周详。关于@@ERROR的介绍可以参见本章后续关于全局变量的内容。

## 分布式事务

### 9.2.3

SQL Server 2012 可支持包括多于一台服务器的事务，它是用 MSDTC（Microsoft分布 事务合作）服务来支持的 有三种方法可使用分布式事务： （1）用 DB-Lib API（应用程序接口）编写分布事务程序，它超出了本书的范围 使用 T-SQL 语法 BEGIN DISTRIBUTED TRANSACTION。 (2) 可用 SETREMOTE PROC TRANSACTION 为单个会话启动分布式事务。 (3) 锁定

### 9.2.4

当多个用户对数据库访问时，为了确保事务完整性和数据库一致性，需要以互斥方式 访问数据项。即当一个事务访问某个数据项时，不允许其他任何事务修改该数据项。这也 是确保事务的隔离性的方法之一，通过并发机制对并发事务之间的相互作用进行控制。主 要的实现技术是封锁机制，只允许事务访问当前该事务持有“锁（lock）”的数据项。一个 锁就是在多用户环境中对某一种正在使用的资源的一个限制，它阻止其他用户访问或修改 资源中的数据。SQL Server 为了保证用户操作结果的一致性，根据最小化维护锁所需资源 的要求，自动对资源设置和释放锁。例如，当用户正在更新一个表时，没有任何其他用户 能修改甚至查看已经更新过的记录。当所有的与该用户相关的更新操作都完成后，锁便会 释放。

### 1．锁定粒度

被锁定的资源单位称为锁定粒度。在 SQLServer 中，锁定粒度按由小到大排列可分为 行、页、扩展盘区、表和数据库。锁定粒度不同，系统的开销也不同，并且锁定粒度与数 据库访问并发是一对矛盾，锁定粒度大，系统开销小，但并发度会降低；锁定粒度小，系 统开销大，但可提高并发度。比如，要访问的数据占某数据页上的50%以上，则在该数据 页上放置单个页级锁所需的系统开销，比在这些数据上放置几十甚至上百个行级锁少得多。 SQL Server 可以根据优化器提供的数据自动进行锁的放置和粒度升级。锁放置与升级 基于2%标准。某事务将访问的数据涉及某数据页上不超过2%的行，则放置行级锁。实际 执行时，发现数据超过页上2%的行，但不超过表中2%的页，则将原来的行级锁升级为一 个页级锁。若超过2%的页，则升级为表级锁。

### 2．锁类型

通常，SQLServer 中有以下三类锁： （1）共享锁 也称为S锁或读锁，是加在正在读取的数据上的，防止别 (Shared) 283 的用户在加锁的情况下修改该数据。一旦读取数据完毕，便立即释放资源上的共享锁，除 非将事务隔离级别设置为可重复读或更高级别，或者在事务生存周期内用锁定提示保留共 享锁。共享锁主要为 SELECT语句分配。可以有多个 SELECT事务同时在同一数据项上获 SQL Server 程序设计 数据库原理与技术（SOLServer2012） 得共享锁，但阻止其他事务对已放置共享锁的数据进行修改，不能放置排他锁。 （2）排他锁 也称为X锁或写锁。事务向数据库中写数据时，将对涉 i（Exclusive）一 及的数据放置排他锁，允许该事务读取和修改这些已获得排他锁的数据，但不允许其他事 284 语句时，会 务再给这些数据放置任何类型的锁和进行任何操作。执行 INSERT、DELETE 给资源放置排他锁。一个资源只能放置一个排他锁 （3）更新锁（Update） 更新锁是共享锁和排他锁的联合应用，在执行UPDATE语 句时使用。UPDATE语句的执行分为两个阶段：数据定位时的读操作和修改已定位数据的 写操作。在数据定位时为数据放置的是共享锁，在定位完成将开始更改数据时，共享锁自 动改为排他锁。更新锁的使用能提升数据读取的并行性。

### 3．死锁

死锁是指两个事务阻塞彼此进程而互相冲突的情况。事务T1 获取了数据项D1 的锁， 事务 T2 获取了数据项D2 的锁，此时，T1 请求获取D2上的锁，T2请求获取D1上的锁， 而 T1、T2 在获得请求的锁前，均不释放自已所获取的锁，结果就是 T1 为了获取 D2上的 锁等待 T2 先释放其上的锁，而 T2 为了获取 D1上的锁等待 T1 先释放其上的锁。这样为 了获取对方资源而又不释放自已占用资源的循环等待，即为死锁现象。 解决死锁问题，可以采用预防和诊断解除两种方法。 预防主要是要消除产生死锁的条件，常用方法有两种：一次封锁法和顺序封锁法。前 者是让事务一次将所有要使用的数据全部加锁：后者是让所有事务按既定顺序对数据对象 加锁。 诊断死锁一般使用超时法和事务等待图法。若事务等待超过规定时间或事务等待图中 出现回路，则认为系统中出现了死锁情况。通常解除死锁采用的方法是最小代价牺牲法。 撤销处理代价最小的死锁事务，释放其占有资源，恢复其他事务的运行。需要注意的是： 被强行撤销的事务要注意恢复其已进行的数据更改，

## SQL Server 变量

### 9.3

变量是 SQL Server 用来在语句之间传递数据的方式之一。SQL Server 中的变量分为全 局变量和局部变量，其中，全局变量的名称以“@@”字符开始，由系统定义和维护；局 部变量的名称以“@”字符开始，由用户自已定义和赋值。

## 全局变量

### 9.3.1

全局变量是系统提供且预先声明的变量。全局变量在所有存储过程中随时有效，用户 利用全局变量，可以访问服务器的相关信息或者有关操作的信息。用户只能引用不能改写， 且不能定义和全局变量同名的局部变量，引用时要在前面加上“@@”标记。所以， @@functions 虽然被称为全局变量，但它们不是变量，也不具备变量的行为，本质上是系 统函数，其语法遵循函数的规则 SQL Server 2012 的所有全局变量共 32 个，见表 9-1。包括配置类@14 个，游标类2 个，元数据类③1个，系统类④4个，系统统计类11个。 表 9-1 SQL Server 中的全局变量 描述

## 全局变量

返回类型 返回自上次启动SQLServer以来连接或试图连接的次数 integer @@CONNECTIONS? 返回自上次启动SQLServer以来CPU的工作时间，单位为毫秒 @@CPU BUSY? integer integer 返回连接中最后打开的游标中当前包含的合格记录的数量 @@CURSOR ROWS? 返回 SET DATEFIRST 参数的当前值，SETDATEFIRST参数指明 @@DATEFIRSTO 所规定的每周的每一天：1 对应星期一，2 对应星期二，以此类 tinyint 推，用7对应星期日 为当前数据库返回当前 timestamp数据类型的值。这一timestamp @@DBTSO varbinary 值保证在数据库中是唯一的 @@ERRORO 返回最后执行的T-SQL语句的错误代码 integer 返回被 FETCH 语句执行的最后游标的状态，而不是任何当前被 @@FETCH STATUS@ integer 连接打开的游标的状态 @@IDENTITYO 返回最后一行插入数据的标识列值 numeric(38,0) @@IDLE? 返回 SQL Server 自上次启动后闲置的时间，单位为毫秒 integer 返回 SQLServer 自上次启动后用于执行输入和输出操作的时间， @@IO BUSY? integer 单位为毫秒 (ID) 返回当前所使用语言的本地语言标识符 @@LANGIDO smallint 返回当前使用的语言名 @@LANGUAGE nvarchar 返回当前会话的当前锁定超时设置（毫秒）。SET @@LOCK TIMEOUTO LOCK TIMEOUT 允许应用程序设置语句等待阻塞资源的最长 integer 时间，单位为毫秒。如未使用 SETLOCK_TIMEOUT，则返回-1 返回 SQLServer 允许的同时用户连接的最大数。返回的数不必为 @@MAX CONNECTI integer ONSO 当前配置的数值 返回 decimal 和 numeric 数据类型所用的精度级别，即该服务器 @@MAX PRECISIONO tinyint 中当前设置的精度 返回当前存储过程执行的嵌套层次（初始值为0 integer @@NESTLEVEL 返回当前 SET选项的信息 @@OPTIONSO integer @@PACK RECEIVED? 返回 SQLServer 自上次启动后从网络上读取的输入数据包数目 integer 返回 SQLServer 自上次启动后写到网络上的输出数据包数目 integer @@PACK SENT? 返回 SQL Server 自上次启动后，在 SQL Server连接上发生的网络 @@PACKET ERRORS? integer 数据包错误数 返回 T-SQL 当前模块的对象标识符(ID)。这些模块可以是存储 @@PROCIDO integer 过程、用户定义函数或触发器 返回受上一语句影响的行数。任何不返回行的语句将这一变量设 @@ROWCOUNTO integer 置为 0 返回运行 SQL Server 的本地服务器名称 nvarchar @@SERVERNAMEO 返回 SQL Server 正在运行的注册表项的名称。如果当前实例为 默认实例，返回MSSQLSERVER；如果当前实例为命名实例，则 @@SERVICENAMEO nvarchar 返回实例名称 285 返回当前用户进程的会话ID smallint @@SPIDO 返回由 SET设置的 TEXTSIZE选项的当前值 integer @@TEXTSIZEO 返回每个时钟周期的微秒数 integer @@TIMETICKS?

SQL Server 程序设计 数据库原理与技术（SOL Server 2012） 续表 描述 返回类型

## 全局变量

返回 SQLServer 自上次启动后，所遇到的磁盘读/写错误数 @@TOTAL ERRORS? integer 返回 SQL Server @@TOTAL READ? integer ：自上次启动后读取磁盘的次数 286 返回 SQL Server 自上次启动后写入磁盘的次数 integer @@TOTAL WRITE? integer 返回当前连接的活动事务数 @@TRANCOUNTO 返回当前 『 SQL Server 安装的版本、处理器体系结构、日期和操 @@VERSIONO nvarchar 作系统 【例9.4】 通过全局变量的引用来查看 SQL Server 的版本、当前所使用的 SQL Server 服务名称和到当前时间为止登录和试图登录的次数。代码如下： 当前所用 SQL Server 版本信息如下：' PRINT --显示版本信息 PRINT @@VERSION --换行 PRINT '目前所用的 SQLSerVer 服务名称为：＇+@@SERVICENAME --显示服务名称 PRINT 到当前时间为止登录和试图登录的次数：' PRINT PRINT @@CONNECTIONS 运行结果如图9-2所示。 SQLQuery1.sql - S...ministrator (55)*X 对象资源管理器详细信息 日PRINT T当前所用SQLServer版本信息如下： @@VERSION--显示版本信息 PRINT --换行 PRINT -显示服务名称 ”目前所用的SQLSerVer服务名称为："+@@SERVICENAME PRINT 到当前时间为止登录和试图登录的次数： PRINT PRINT @@CONNECTIONS

100 % 消息 当前所用SQLServer版本信息如下： Microsoft SQL Server 2012 (SP1)- 11.0.3128.0 (X64) Copyright (c) Microsoft Corporation Enterprise Edition (64-bit) on Windows HT 6.1 <X64> (Build 7601: Service Pack 1)

目前所用的SQLSerVer服务名称为：MSSQLSERVER 到当前时间为止登录和试图登录的次数： 2045 100 % 查询已成功...「SKY-20170310IRL(11.0SP1)【SKY-20170310IRL\Admin...【student「00:00:00「0行 图 9-2 全局变量引用的结果

## 局部变量

### 9.3.2

局部变量是用户自已定义的，只在定义它的批处理或可编程对象中使用。SQL Server 的可编程对象主要指视图、函数、存储过程、触发器等可通过 SQL Server 编程来定义其功 能的数据库对象。可以创建、读取、写入局部变量，在操作和存储数据及可编程对象间传 递数据。

### 1．局部变量声明

使用一个局部变量之前，必须使用DECLARE语句来声明这个局部变量，给它指定一 个变量名和数据类型，对于数值变量，还需要指定其精度和小数位数。DECLARE 语句的 语法格式为： DECLARE @局部变量 数据类型［1n] 局部变量名总是以“@”符号开始，最多可以包含128个字符，必须符合 SQL Server 标识符命名规则。局部变量的数据类型可以是系统数据类型，也可以是用户自定义数据类 型，但不能把局部变量指定为 text、ntext 或 image 数据类型。在一个 DECLARE 语句中 语句。 【例9.5】 声明各类局部变量。代码如下： @SNO char(12)， @SNAME Varchar(20) DECLARE @SBIRTH DATETIME=GETDATE() DECLARE @SCORE DECIMAL(6,1)=0.0 DECLARE --声明一个名为@tableStu的表变量 @tablestu DECLARE TABLE SID int not null, Sname not null ) varchar(15)

### 2．局部变量赋值

所有局部变量在声明的同时可以为其指定一个初始值，如例 9.5中的第二个变量

## @SBIRTH、第三个变量@SCORE

在声明同时分别被指定了初始值 GETDATEO和 0.0。若 没有指定，则被初始化为NULL，如例 9.5 中的其他变量。 还可以使用SELECT语句或SET语句将一个不是NULL的静态值赋给已声明的变量。 一条 SELECT语句一次可以为多个局部变量赋值；一条 SET语句一次只能为一个局部变量 赋值。 （1）用SELECT为局部变量赋初值的语法格式如下： @变量名=表达式［，n] SELECT 如果使用一个SELECT语句对一个局部变量赋值时，这个语句返回了多个值，则这个 局部变量将取得该 SELECT语句所返回的最后一个值。此外，使用 SELECT语句时，如果 省略赋值号（=）及其后面的表达式，则可以将局部变量的值显示出来。例如: @ages int,@sname char(8) DECLARE @ages=10，@sname='张敏' --赋值 SELECT '姓名：'，@sname，'年龄：'，@ages --显示变量值 SELECT （2）用SET语句为局部变量赋初值的语法格式如下： 287 @变量名=表达式［，n] SET SET语句的功能是将表达式的值赋给局部变量。其中，表达式是 SQL Server 的任何有

SQL Server 程序设计 数据库原理与技术（SOL Server 2012） 效的表达式。例如: DECLARE @str char(20) SET @str='这是一个试验。 288 PRINT @str （3）类似于 C，SQL Server 2012 支持对变量的复合赋值表达，如 十=、*=。例如: SET @a+=1 相当于: SET @a=@a+1

### 3．局部变量的作用域

局部变量的作用域指可以引用该变量的范围。局部变量的作用域从声明它的地方开始 到声明它的批处理或可编程对象结束。也就是说，局部变量只能在声明它的批处理、函数、 存储过程或触发器中使用，一旦这些批处理或对象结束，局部变量将随之自动消亡 声明一个局部变量dep name，把 student数据库中的“系部”表中系部代码 【例9.6】 为 0l 的系部名称赋给局部变量 dep_name，并输出。 代码如下: USE student GO --声明局部变量 @dep name varchar(30) DECLARE @dep_name=系部名称 FROM 系部 --为变量赋值 系部代码=＇01' WHERE SELECT '系部表中系部代码为''01''的系部名称为：'+@dep_name --引用变量输出字符串 PRINT GO --该批处理结束，局部变量@dep name 自动清除 --输出字符串 GO 运行结果如图9-3所示。 对象资源管理器详细信息 SQLQuery1.sql - S...ministrator (55)*X USE student GO 日DECLARE@depP_namevarchar（30）--声明局部变量 SELECT@deP_name=系部多秘FROM系部WHERE系部代码="01”--为变量赋值 PRINT"系部表中系部代码为""01""的系部名称为："+@deP_name--引用变量输出字符串 GO --该批处理结束，局部变量@dep_name自动清除 --输出字符串 GOl 100 % 消息 系部表中系部代码为01"的系部名称为：计算机系 消息137，级别15，状态2，第2行 必须声明标量变量“@dep_name"。

100 % A查询已完成...【SKY-20170310IRL(11.0SP1)「SKY-20170310IRL\Admini...[student「00:00:000行 图 9-3 局部变量的作用域

# SQL语言流程控制

### 9.4

流程控制语句是用来控制程序执行顺序的命令，这些命令包括条件控制语句、无条件 转移语句、循环语句。使用这些语句，可以实现结构化程序设计 ）语句块

### 9.4.1

BEGIN..END 在条件和循环等流程控制语句中，要执行两个或两个以上的T-SQL语句时就需要使用 BEGINEND 语句。BEGINEND语句将多个 T-SQL 语句组合成一个语句块，并将它们 作为一个整体来处理。BEGINEND语句块可以嵌套 BEGINEND语句的语法格式为： BEGIN {语句组} END

## IF.ELSE 语句

### 9.4.2

在程序中，经常需要根据条件指示 SQL Server 执行不同的操作和运算，也就是进行程 序分支控制。SQL Server 利用 IFELSE 语句使程序有不同的条件分支，从而实现分支条 件程序设计。 IFELSE语句的语法格式为： IF布尔表达式 语句1 [ELSE 语句21

一个 SELECT语句，则必须使用圆括号把这个 SELECT语句括起来。语句1和语句2可以

是：先求布尔表达式的值，如果布尔表达式的值为TRUE，则执行语句1，否则执行语句2。 若无ELSE，如果测试条件成立，则执行语句1，否则执行IF语句后面的语句。 【例9.7】 ，“，“，丑碧S由 ，“，“，“，“，‘“ 职称的教师”。 代码如下： UsE student GO 教师 WHERE 职称='教授’OR 职称='副教授') EXISTS (SELECT * FROM IF 289 BEGIN ‘具有高级职称的教师有： SELECT 姓名，学历,职务,职称 FROM 教师 WHERE 职称='教授’OR 职称='副教授' SELECT

SQL Server 程序设计 数据库原理与技术（SOL Server 2012） END ELSE BEGIN ‘没有高级职称的教师 PRINT 290 END GO 运行结果如图9-4所示。 SQLQuery1.sql - S..ministrator (55))*X 对象资源管理器详细信息 USE student GO EXISTS（SELECT*FROM教师WHERE职称="教授”OR职称="副教授） BIF BEGIN SELECT”具有高级职称的教师有：" 姓名，学历，职务，职称FROM教师WHERE职称="教授”OR职称=副教授 SELECT END ELSE BEGIN PRINT”没有高级职称的教师 END GO 100 % 结果 消息 (无列名) 具有高级职称的教师有： 姓名 学历 职称 主任 教授 张学杰 硕士 王钢 博士 副教授 教师 副主任 周红梅 博士 副教授 SKY-20170310IRL(11.0SP1)「SKY-20170310IRL\Admini...student[00:00:00|4行 查询已成功

图 9-4 使用IFELSE语句示例

## CASE 结构

### 9.4.3

如果对于一个条件来说可能有多于两种的情况，那么对于不同的情况就应该执行不同 的操作。在程序设计中，遇到这样的情况，使用CASE语句就比较简单。CASE语句具有 两种格式。

### 1．简单 CASE 表达式

简单 CASE表达式语法格式为： CASE 表达式值 1 THEN 结果表达式 1 WHEN 表达式值 2 THEN [WHEN 结果表达式 2 [.. 结果表达式 nl [ELSE END WHEN子句的表达式值比较，直到 其执行过程是：用条件表达式的值依次与每一个 与一个表达式值完全相同时，便将该WHEN 子句指定的结果表达式返回。如果没有任何一 个WHEN子句的表达式值和条件表达式值相同，这时，如果存在ELSE子句，便返回ELSE 子句之后的结果表达式；如果不存在ELSE子句，便返回一个NULL 值。 【例9.8】 使用简单CASE结构实现以下功能：输出“课程名”，而且在“课程名”后 添加“备注”。 代码如下： UsE student GO 课程名，备注= SELECT 课程名 CASE '大学英语’ '在一、二年级分四个学期修读' WHEN THEN '包括上下两部分，在一年级修读' '高等数学' WHEN THEN '可选择在一年级任一学期修读' 计算机导论 THEN WHEN '数据库原理' 计算机及相关专业必修课' WHEN THEN '其他' ELSE END FROM i GO 运行结果如图9-5 所示。 SQLQuery1.sql - S...ministrator (55))*X 对象资源管理器详细信息 USE student GO 日SELECT课程多，备注= CASE课程名 WHEN”大学英语’ THEI"在一、二年级分四个学期修读” WHEN"高等数学THEN包括上下两部分，在一年级修读” WHEN”数据库原理”T TN计算机及相关专业必修课 ELSE"其他 END FROM课程 GO 100 % 围 结果 消息 课程名 备注 大学英语 在一、二年级分四个学期修读 高等数学 包括上下两部分，在一年级修读 计算机导论 可选择在一年级任一学期修读 数据库原理 计算机及相关专业必修课 其他 人工智能 其他 国际贸易学 其他 环境经济学 查询已成功...「SKY-20170310IRL（11.0SP1「SKY-20170310IRL\Admini...student「00:00:00「7行 图 9-5 简单 CASE 表达式示例

### 2.． 搜索 CASE 表达式

搜索 CASE 表达式语法格式为: CASE 291 逻辑表达式 1 THEN 结果表达式 1 WHEN 逻辑表达式 2 THEN 结果表达式 2 [WHEN [..

SQL Server 程序设计 数据库原理与技术（SOLServer2012） 结果表达式 nl [ELSE END 其执行过程是：测试每个WHEN子句后的逻辑表达式，如果结果为TRUE，则返回相 292 应的结果表达式；否则检查是否有 ELSE 子句，如果存在 ELSE 子句，便返回 ELSE 子句 之后的结果表达式；如果不存在ELSE子句，便返回一个NULL 值。 【例9.9】使用搜索CASE表达式实现以下功能：根据“学生”表分别输出“学号”“姓 名”“入学时间”，并根据入学时间判定学生所在年级。 代码如下： USE student GO 学号，姓名，入学时间，年级= SELECT DISTINCT CASE year（入学时间)='2014' '三年级' THEN WHEN year（入学时间)='2015' '二年级' THEN WHEN END 学生 FROM : GO 运行结果如图9-6所示 SQLQuery1.sql - S...ministrator (55)*X 对象资源管理器详细信息 USE student GO 日SELECTDISTINCT学号，姓名，入学时间，年级= CASE WHENyear（入学时间)="2014'THEN"三年级" WHENyear(入学时间）="2015'THEN'二年级” END FROM 学生 GO 100 % 结果 脂消息 姓名 学号 年级 入学时间 张斌 三年级 2014-09-01 00:00:00.000 140101001001 三年级 李岚 2014-09-01 00:00:00.000 140101001011 三年级 贾凌云 140201001001 2014-09-01 00:00:00.000 三年级 向雪林 140202002001 2014-09-01 00:00:00.000 周红瑜 150102002001 二年级 2015-09-01 00:00:00.000 李晟 二年级 150102002007 00:00:00.000 2015-09-01 二年级 周春梅 150102002018 00:00 :00.000 2015-09-01 张雪琪 二年级 150103001001 2015-09-01 00:00:00.000 李艾一 二年级 150103001003 2015-09-01 00:00:00.000 刘伟 二年级 2015-09-01 00:00:00.000 10 150103001012 SKY-20170310IRL(11.0SP1)「SKY-20170310IRL\Admini...|student「00:00:0010行 查询已成..

图 9-6 搜索 CASE 表达式示例

## WAITFOR 语句

### 9.4.4

语句指定触发语句块、存储过程或事务执行的时间、时间间隔或事件。其 WAITFOR 语法格式为： WAITFOR DELAY＇时间＇ITIME 其中，DELAY指定一段时间间隔过去之后执行一个操作。TIME表示从某个时刻开始 执行一个操作。时间参数必须为可接受的DATETIME数据格式。在 DATETIME数据中不 允许有日期部分，即采用HH:MM:SS的格式。

## 使用 WAITFOR 实

【例9.10】 实现以下功能：根据“学生”表输出“系部代码”为02 的“学号”“姓名”“出生日期”，在输出之前等待4秒。 代码如下： UsE student GO WAITFOR DELAY ＇00:00:04' 学号，姓名，出生日期 FROM 学生 WHERE 系部代码=＇02 SELECT GO

## PRINT 语句

### 9.4.5

SQL SerVer 向客户程序返回信息的方法除了使用 SELECT语句外，还可以使用PRINT 语句，其语法格式为： PRINT 字符串I函数I局部变量I全局变量 【例9.11】 PRINT语句示例 代码如下： UsE student GO DECLARE @str char(3O) SET @str='欢迎使用选课管理信息系统 PRINT @str GO 运行结果如图9-7所示。 SQLQuery1.sql - S...ministrator (55))*X USE student GO DECLARE @str char(30) SET@str="欢迎使用选课管理信息系统 PRINT @str GO 100 % 消息 欢迎使用选课管理信息系统 293 100 % SKY-20170310IRL\VAdmini...|student00:00:00「0行 0SP1)

图 9-7 PRINT语句示例

SQL Server 程序设计 数据库原理与技术（SOL Server2012）

说明：使用PRINT 语句输出的信息出现在“消息”窗格，使用 SELECT 语句输出的 信息出现在“结果”窗格。 294

## WHILE语句

### 9.4.6

在程序中当需要多次重复处理某项工作时，就需要使用WHILE循环语句。WHILE语 句通过逻辑表达式来设置一个循环条件，当条件为真时，重复执行一个SQL语句或语句块; 否则退出循环，继续执行后面的语句。WHILE语句的语法格式为： WHILE 逻辑表达式 BEGIN 语句块1 [BREAK] 语句块 2 [CONTINUE] 语句块3 END

其中，逻辑表达式用来设置循环执行的条件。当表达式取值为TRUE时，循环将重复 执行；取值为 FALSE 时，循环将停止执行。如果逻辑表达式中包含一个 SELECT 语句, 必须将该SELECT语句包含在一对小括号中。 若要提前退出循环，可选 命令，并将控制权转移给循环之后的语句。选 BREAK 命令可使程序直接跳回到 WHILE命令行，重新执行循环，忽略CONTINUE CONTINUE 之后的语句。 循环允许嵌套，在嵌套循环中，内层循环的BREAK命令将使控制权转移到外一层的 循环并继续执行。 使用 WHILE语句实现以下功能：求2～10 的平方。 【例9.12】 代码如下： DECLARE @counter int SET @counter=2 WHILE @counter<=l0 BEGIN PRINT POWER(@counter,2) SET @counter=@counter+l END GO 运行结果如图9-8所示， SQLQuery1.sql - S...ministrator (55)*X 日DECLARE @counter int SET @counter=2 白WHILE @counter<=10 BEGIN PRINT POWER(@counter,2) SET @counter=@counter+l END GO 100 % 消息 16 25 36 49 64 81 100 100 % 0SP1) SKY-20170310IRLVAdmini...student「00:00:00「0行 图 9-8 WHILE语句示例

## 应用举例

### 9.5

前面已经介绍了SQL Server 的批处理、脚本、注释和事务的概念，并学习了流程控制 语句。下面将以实际的“选课管理信息系统”数据库为例，来加深对上述概念的理解。 在查询窗口中下创建脚本文件chaxun.sql，用来输出所有学生各门课程的成绩，并将 成绩转换为五级等级制，运行结果如图9-9所示。操作步骤如下： （1）在查询窗口中输入以下代码: USE student GO /*下面的批处理用来输出所有学生的学号、姓名及其各门课程的课程名和成绩 并将成绩转换为五级等级。*/ SELECT A.学号,A.姓名,C.课程名,B.成绩,等级= --CASE语句用来添加课程的备注 CASE 成绩>=90 and 成绩<=100 THEN ‘优秀' WHEN 成绩>=80 and 成绩<90 THEN WHEN '中等' 成绩>=70 and 成绩<80 WHEN THEN '及格' 成绩>=60 and 成绩<70 WHEN THEN 成绩>=0 and 成绩<60 '不及格' WHEN THEN '成绩有误' ELSE END 课程注册 AS B FROM 学生 AS A JOIN 295 ON A.学号=B.学号 JOIN 课程 AS C ON B.课程号=C.课程号

SQL Server 程序设计 数据库原理与技术（SOL Server 2012） ORDER BY A.学号 GO

SQLQuery1.sql -S...ministrator (55))*X 对象资源管理器详细信息 296 USE student GO 日SELECT学号，息姓多，C课程名，B成绩，等级= -CASE语苟用来添加课程的备注 CASE WHEN成绩>=90and成绩<=100THEN优秀 WHEN成绩>=80and成绩<90THEN良好” WHEN成绩>=70and成绩<80THEN"中等” WHEN成绩>=60and或绩<70THEN及格” WHEN成绩>=0and成绩<60THEN”不及格" ELSE成绩有误” END FROM学生ASAJOIN课程注册ASB ONA学号-B.学号 JOIN课程ASC ONB.课程号=C.课程号 LORDER BYA学号 GO 100 % 结果 消息 学号 姓名 课程名 成绩 等级 张斌 良好 大学英语 87 140101001001 高等数学 张斌 74 140101001001 张斌 计算机导论 中等 71 140101001001 及格 张斌 数据库原理 69 140101001001 优秀 张斌 人工智能 140101001001 90 大学英语 不及格 李岚 56 140101001011 高等数学 李岚 及格 68 140101001011 计算机导论 中等 李岚 77 140101001011 SKY-20170310IRL(11.0SP1)/SKY-20170310IRL\Admini...|student「00:00:00「36行 查询已成功执行。

图 9-9 案例应用示例

（2）选择菜单栏中的“文件”→“保存”命令，打开“另存文件为”对话框，输入文 件名chaxun.sql，单击“保存”按钮，如图9-10所示。 另存文件为 桌面 搜素桌面 新建文件夹 组织 下载 桌面 系统文件夹 遇最近访问的位置 家庭组 系统文件夹 视频 Administrator 图片 系统文件夹 国 文档 计算机 迅雷下载 系统文件夹 音乐 网络 chaxun.sq 文件名(N): SQL文件(*.sq) 保存类型D：

保存(S) 取消 隐藏文件夹

图 9-10 “另存文件为”对话框 练习题

### 1．什么是批处理？批处理的结束标志是什么？

### 2．什么是事务？事务有哪些特性?

### 3．什么是全局变量？什么是局部变量？

### 4．怎样给变量赋值?

### 5．编写程序，求2～500 的所有素数。

### 6．编写程序，求快递运费。快递运费的计算方法为：首重3千克以内（含3千克）,

运费15元；3～5千克（含5千克），运费为首重运费1.5倍；5～10千克（含10千克）， 运费为首重运费2倍；10～20千克（含20千克），运费为首重运费2.8倍；20千克以上， 运费面议。

### 7．完成本章的所有实例。

297

SQL Server 程序设计

## 存诸过程与触发器
