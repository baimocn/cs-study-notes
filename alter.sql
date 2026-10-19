alter table Questions1 add [错次] int not null default 0;
GO
SELECT 题号, 连续答对次数, [错次] FROM Questions1 WHERE 题号='C1-T1';
GO
