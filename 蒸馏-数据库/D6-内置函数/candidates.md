# D6 内置函数 · 五候选池（ch08 通读产出）

> 记法红线：按"输入→返回值"原子记帧，不整段抄文档。
> 每条候选标注书内支撑位置（供 V1 双小节验证用）。

## C1 聚合函数对 NULL 的处理差异 + COUNT(*) vs COUNT(列) vs COUNT(DISTINCT 列)
- 书内支撑：8.1.1 五函数定义（AVG/COUNT/MAX/MIN/SUM，均带 ALL|DISTINCT 参数）；例8.1（AVG+GROUP BY 算每生平均分）；例8.2（COUNT(DISTINCT 课程号) 算选课数）；例8.3（MAX 子查询选每课最高分行）；章末练习5、7 复用 AVG/COUNT。
- 帧示例：COUNT(*)→全行数（含 NULL 行，空表=0）；COUNT(列)→非 NULL 值个数；COUNT(DISTINCT 课程号)→去重后非 NULL 个数；AVG/SUM/MAX/MIN→忽略 NULL 后运算。
- 教材瑕疵：参数描述 OCR 乱（"返回唯一非空值的数量"错复制给 MAX/MIN/SUM）；SUM 空集返回 NULL 教材**未明说**。

## C2 字符串函数（LEN / LEFT / RIGHT / SUBSTRING / CHARINDEX / PATINDEX / REPLACE / UPPER / LOWER / LTRIM / RTRIM / CONCAT）
- 书内支撑：8.1.6 按五小类分述；例8.26（LEFT('command',4)='comm'）；例8.27（CHARINDEX('雪',姓名)>0 筛姓名）；例8.28（PATINDEX('%tt%','wwttyy')=3）；例8.29（CONCAT('hello',NULL,'world')='helloworld'，NULL 当空串）；章末练习6（字符串处理四连）。
- 钩子帧：CONCAT 把 NULL 当空串；LEN 不含尾随空格；CHARINDEX/PATINDEX 找不到返回 0、>0 即命中。

## C3 日期时间函数（GETDATE / YEAR / MONTH / DAY / DATENAME / DATEFROMPARTS / EOMONTH）
- 书内支撑：8.1.3 十二个函数 + 表8-1 datepart 参数表；例8.6（GETDATE()→'2017-01-15 22:38:16.333'）；例8.7-8.9（DAY=15 / MONTH=1 / YEAR('01/15/2017')=2017）；例8.10（DATEFROMPARTS(2017,1,15)='2017-01-15'）；例8.13（EOMONTH('2017-01-16')='2017-01-31'、EOMONTH(...,1)='2017-02-28'）；章末练习5、7 要求用日期函数取年份算年级/年龄。
- 钩子帧：YEAR/MONTH/DAY 返回 **int**，DATENAME 返回**字符串**（weekday '12/20/2016'→'星期二'）。

## C4 数学函数（ABS / CEILING / FLOOR / ROUND / POWER / SQUARE / SQRT / PI）
- 书内支撑：仅 8.1.4 一节（V1 双小节支撑弱，如实标记）；例8.15（ABS(-12)=12）；例8.17（CEILING(56.3)=57，CEILING(-56.3)=-56）；例8.19（FLOOR(56.3)=56，FLOOR(-56.3)=-57）；例8.20-8.23（POWER(2,3)=8、SQUARE(5)=25、SQRT(16)=4）；例8.18（DEGREES(PI())=180）；例8.21（ROUND(56.34,1)=56.30，ROUND(56.34,-1)=60）。
- 钩子帧：CEILING 向大取整、FLOOR 向小取整——负数方向不反转；ROUND 的 y 为负=小数点**左侧**舍入。

## C5 类型转换 + 2012 新增标量函数（CAST / CONVERT / TRY_CONVERT / PARSE / CHOOSE / IIF）
- 书内支撑：8.1.7 系统函数（CAST/CONVERT 定义）；例8.31（CAST('123' AS int)+20=143）；例8.33 顺带示范 convert(varchar(100),出生日期,23) 去时间；8.1.9 新增函数：例8.34（PARSE）、例8.35（TRY_CONVERT(float,'ttt')→NULL）、例8.36（CHOOSE(3,'A','B','C','D')='C'）、例8.37（IIF(3>2,'T','F')='T'）。
- 钩子帧：TRY_CONVERT 转不动→返回 NULL 不报错；CONVERT 多一个 style 参数管日期格式。
