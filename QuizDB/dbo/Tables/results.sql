CREATE TABLE [dbo].[results] (
    [id]          INT            IDENTITY (1, 1) NOT NULL,
    [question_id] INT            NULL,
    [user_answer] NVARCHAR (500) NULL,
    [is_correct]  BIT            NULL,
    [test_time]   DATETIME       DEFAULT (getdate()) NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    FOREIGN KEY ([question_id]) REFERENCES [dbo].[questions] ([id])
);


GO

