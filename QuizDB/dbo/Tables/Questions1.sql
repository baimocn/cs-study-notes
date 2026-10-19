CREATE TABLE [dbo].[Questions1] (
    [题号]     VARCHAR (5)    NOT NULL,
    [学科]     NVARCHAR (5)   NOT NULL,
    [内容]     NVARCHAR (MAX) NOT NULL,
    [答案]     NVARCHAR (MAX) NOT NULL,
    [连续答对次数] INT            NOT NULL,
    [错次]     INT            DEFAULT ((0)) NOT NULL,
    CONSTRAINT [PK_Questions1] PRIMARY KEY CLUSTERED ([题号] ASC)
);


GO

