INSERT INTO Questions1 (题号, 学科, 内容, 答案, 连续答对次数) VALUES
('D1-T2', N'数据库', N'UNIQUE约束允许出现空值吗？', N'允许。UNIQUE只强制唯一，允许空值；PRIMARY KEY才不允许空值', 0),
('D1-T3', N'数据库', N'关系模型由哪三部分组成？', N'数据结构、关系操作、数据完整性', 0),
('D2-T1', N'数据库', N'写出创建数据库teacher2的T-SQL语句', N'CREATE DATABASE teacher2 ON PRIMARY(NAME=teacher2_data, FILENAME=...)', 0),
('D3-T1', N'数据库', N'WHERE和HAVING的区别是什么？', N'WHERE作用于行，HAVING作用于组；WHERE在GROUP BY前执行，HAVING在后', 0),
('D4-T1', N'数据库', N'ODBC四层结构是什么？', N'应用程序、驱动程序管理器、DBMS驱动程序、数据源', 0),
('C1-T1', N'高级语言', N'设int i=2,j; 执行j=i++*3+++i; 后j的值是多少？', N'后缀先用后加，前缀先加后用', 0),
('C1-T2', N'高级语言', N'字符串"a\tb\065"在内存中占多少字节？', N'转义字符算1个字符，\ddd是八进制转义', 0),
('C5-T1', N'高级语言', N'指针与一维数组的四种等价写法是什么？', N'a[i] = *(a+i) = p[i] = *(p+i)', 0),
('C8-T1', N'高级语言', N'fopen的六种模式中，w和a有什么区别？', N'w清空重写，a末尾追加不清空；r必须文件已存在', 0);

SELECT COUNT(*) AS Total FROM Questions1;
GO
