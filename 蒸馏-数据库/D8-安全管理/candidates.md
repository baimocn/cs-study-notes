# D8 候选池（ch11 SQL Server 2012 安全管理）

- 来源：`数据库原理-章节\ch11-SQLServer2012安全管理.md`（537 行；§11.1-11.3 安全主体 + §11.4-11.9 备份还原/导入导出）
- 筛法：全章扫读 → 初筛 8 处 → 按单元边界（安全管理=验证/账号/角色/权限）收敛为 5 候选。
- 三重验证（V1 教材适配双小节 / V2 新题 / V3' 考试杀伤力）结果见 `verified.md`。

## C1 两种身份验证模式
- 书中锚点：§11.1.1（行 11-19）、图 11-1
- 原始素材：Windows 验证（只认能登录 Windows 服务器的用户）/ 混合验证（Windows 用户 + 独立 SQL Server 用户都可登录）；修改验证模式后必须停止并重新启动 SQL Server 服务才生效；Win95/98 无法验证 NT 账号只能用混合（陈旧背景）。
- 初判钩子：判据 = 是否放行"SQL Server 独立登录账号"。
- 初判杀伤力：高（简答常客，练习题第 1 题原题）。

## C2 登录名 vs 数据库用户 两级模型
- 书中锚点：§11.2 引言（行 37）、§11.3.1（行 105-127）
- 原始素材：Login Name 属服务器层、本身不能访问数据库；User Name 由登录名映射而来、存于 sysusers 表；一个登录账号在一个数据库中只能有一个用户账号，可在不同数据库各有一个；有登录名≠能对库中对象做插入更新；sa 超级账号安装后密码为空，装完第一件事是设密码。
- 初判钩子：两级门禁——登录名=大门钥匙，数据库用户=房间通行证。
- 初判杀伤力：高（选择+简答双题型，练习题第 2 题原题）。

## C3 角色：服务器角色与数据库角色
- 书中锚点：§11.1.2（行 23-25）、表 11-1（行 61-65）、§11.3.2（行 129-169）、表 11-2（行 149）
- 原始素材：角色=权限的集合（类似 Windows 用户组）；服务器角色 9 个固定（sysadmin/serveradmin/setupadmin/securityadmin/processadmin/dbcreator/diskadmin/bulkadmin/public）；数据库角色应用于单个数据库，分数据库角色与应用程序角色（后者不含成员）；固定数据库角色 10 个（public/db_owner/db_accessadmin/db_securityadmin/db_ddladmin/db_backupoperator/db_datareader/db_datawriter/db_denydatareader/db_denydatawriter）；public 人人必有，新用户自动加入。
- 初判杀伤力：高（填空/选择考固定角色名单与 public 特殊性）。
- 留疑：表 11-1 中 Processadmin 描述与 Setupadmin 重复，疑原书排印或 OCR 错（见 verified.md 留痕）。

## C4 权限三分类：对象权限 / 语句权限 / 隐含权限
- 书中锚点：§11.3.3 之 1（行 177-180）
- 原始素材：对象权限=对表/视图/存储过程等对象的操作权（表/视图：SELECT INSERT UPDATE DELETE；字段：SELECT UPDATE；存储过程：EXECUTE）；语句权限=数据定义类语句权（CREATE TABLE、CREATE DEFAULT、CREATE RULE、CREATE VIEW、CREATE PROCEDURE、BACKUP DATABASE、BACKUP LOG）；隐含权限=系统预定义（sysadmin 成员、dbo、对象所有者），不需要也不能设置。
- 初判杀伤力：高（简答"三种权限"为练习题第 3 题原题；对象/语句归类是选择题陷阱）。

## C5 GRANT/REVOKE/DENY 三动词 + 权限继承与 DENY 优先
- 书中锚点：§11.3.3 之 2/3（行 181-188）；GRANT/REVOKE/DENY 英文词见于表 11-2 db_ddladmin 行（行 149）
- 原始素材：权限管理三内容=授予（允许执行）/拒绝访问（即使被授予或继承获得也不允许）/取消（不允许执行）；"不允许"与"拒绝"不同——不允许可经加入角色重新获得允许，拒绝后无法再经角色获得；三种权限冲突时拒绝访问权限起作用；用户继承所属角色的权限；用户分属多角色时权限取并集，但只要有一个拒绝即为拒绝。
- 初判钩子：权限账本——GRANT 存入、REVOKE 划掉、DENY 盖冻结章。
- 初判杀伤力：极高（三动词辨析是本章最易失分点，REVOKE/DENY 区分几乎必考）。

## 落选速记（留痕详见 verified.md）
- 备份还原体系（§11.4-11.5）、维护计划（§11.8）、数据导入导出（§11.9）：属容灾/数据移动主题，非权限管理主线 → 移出 D8 候选。
- SSMS 逐击操作步骤、图 11-1~11-37 截图描述：操作性冗余，考试只考概念与少量授权语义。
- Windows 95/98 注意、C2 审核跟踪、登录审核选项：陈旧或边角，降为词条。
