CREATE TABLE [dbo].[分数表] (
    [学科]  NVARCHAR (5) NOT NULL,
    [分数]  INT          NOT NULL,
    [及格率] INT          NOT NULL,
    PRIMARY KEY CLUSTERED ([学科] ASC)
);


GO

