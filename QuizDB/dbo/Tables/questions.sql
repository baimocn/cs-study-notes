CREATE TABLE [dbo].[questions] (
    [id]                  INT            IDENTITY (1, 1) NOT NULL,
    [unit]                NVARCHAR (20)  NOT NULL,
    [qtype]               NVARCHAR (20)  NOT NULL,
    [question]            NVARCHAR (500) NOT NULL,
    [answer]              NVARCHAR (500) NOT NULL,
    [wrong_count]         INT            DEFAULT ((0)) NULL,
    [consecutive_correct] INT            DEFAULT ((0)) NULL,
    [status]              NVARCHAR (10)  DEFAULT (N'未测') NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

