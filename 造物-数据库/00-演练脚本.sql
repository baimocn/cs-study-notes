/* ============================================================
   工具演练脚本（不是 A1 的答案！）
   用途：只验证一件事 —— 你能不能把一段 SQL 从文件跑进 SQL Server
   它自己建库、自己用完、可以随时删掉，不碰你任何现有库
   ============================================================ */

USE master;
GO

IF DB_ID(N'_工具演练') IS NOT NULL
    DROP DATABASE [_工具演练];
GO

CREATE DATABASE [_工具演练];
GO

USE [_工具演练];
GO

CREATE TABLE 科目(
    科目ID   INT           IDENTITY(1,1) PRIMARY KEY,
    科目代码 CHAR(5)       NOT NULL UNIQUE,
    科目名称 NVARCHAR(30)  NOT NULL
);
GO

INSERT INTO 科目(科目代码, 科目名称) VALUES
    ('13009', N'数据库原理与技术'),
    ('13013', N'高级语言程序设计');
GO

SELECT 科目ID, 科目代码, 科目名称 FROM 科目;
GO
