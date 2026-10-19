/*
 * quiz.c - C语言 + 数据库 连接演示
 * 
 * 这个程序展示了C如何通过ODBC连接SQL Server数据库：
 * 1. 连接数据库
 * 2. 从questions表抽题
 * 3. 让用户答题
 * 4. 判断对错，记录到results表
 * 5. 更新questions表的状态
 *
 * 编译：gcc quiz.c -o quiz.exe -lodbc32
 * 运行：quiz.exe
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <sql.h>
#include <sqlext.h>

/* 最大缓冲区大小 */
#define MAX_SQL 1024
#define MAX_ANSWER 500
#define MAX_QUESTION 500

/* 打印ODBC错误信息 */
void print_error(SQLSMALLINT handleType, SQLHANDLE handle) {
    SQLCHAR sqlState[6], errorMsg[256];
    SQLINTEGER nativeErr;
    SQLSMALLINT msgLen;
    
    if (SQLGetDiagRec(handleType, handle, 1, sqlState, &nativeErr, 
                      errorMsg, sizeof(errorMsg), &msgLen) == SQL_SUCCESS) {
        printf("[ERROR] %s: %s\n", sqlState, errorMsg);
    }
}

/* 连接数据库 */
SQLHDBC connect_db(SQLHENV *env, SQLHDBC *dbc) {
    SQLRETURN ret;
    
    /* 分配环境句柄 */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, env);
    if (ret != SQL_SUCCESS && ret != SQL_SUCCESS_WITH_INFO) {
        printf("无法分配环境句柄\n");
        return NULL;
    }
    
    /* 设置ODBC版本 */
    SQLSetEnvAttr(*env, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    
    /* 分配连接句柄 */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, *env, dbc);
    if (ret != SQL_SUCCESS && ret != SQL_SUCCESS_WITH_INFO) {
        printf("无法分配连接句柄\n");
        return NULL;
    }
    
    /* 连接字符串 - 这里用Windows认证连接本地SQL Server */
    SQLCHAR connStr[] = "DRIVER={ODBC Driver 18 for SQL Server};"
                        "SERVER=localhost;"
                        "DATABASE=QuizDB;"
                        "UID=;"
                        "PWD=;"
                        "Trusted_Connection=yes;"
                        "Encrypt=no;";
    
    /* 建立连接 */
    ret = SQLDriverConnect(*dbc, NULL, connStr, SQL_NTS, 
                           NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
    
    if (ret != SQL_SUCCESS && ret != SQL_SUCCESS_WITH_INFO) {
        print_error(SQL_HANDLE_DBC, *dbc);
        return NULL;
    }
    
    printf("[OK] 数据库连接成功！\n");
    return *dbc;
}

/* 获取未测或待复测的题目数量 */
int get_question_count(SQLHDBC dbc) {
    SQLHSTMT stmt;
    SQLINTEGER count = 0;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)"SELECT COUNT(*) FROM questions WHERE status != N'已过关'", SQL_NTS);
    if (SQLFetch(stmt) == SQL_SUCCESS) {
        SQLGetData(stmt, 1, SQL_C_SLONG, &count, 0, NULL);
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    return count;
}

/* 随机抽取一道题，返回题号 */
int get_random_question(SQLHDBC dbc) {
    SQLHSTMT stmt;
    SQLINTEGER id = 0, total;
    int target;
    
    total = get_question_count(dbc);
    if (total == 0) return 0;
    
    /* 随机选一道 */
    target = rand() % total + 1;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    /* 用TOP + 子查询实现随机抽题 */
    SQLExecDirect(stmt, (SQLCHAR*)
        "SELECT TOP 1 id FROM ("
        "  SELECT ROW_NUMBER() OVER (ORDER BY id) AS rn, id "
        "  FROM questions WHERE status != N'已过关'"
        ") AS sub WHERE rn = ?",
        SQL_NTS);
    
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &target, 0, NULL);
    SQLExecute(stmt);
    
    if (SQLFetch(stmt) == SQL_SUCCESS) {
        SQLGetData(stmt, 1, SQL_C_SLONG, &id, 0, NULL);
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    return id;
}

/* 显示一道题 */
void show_question(SQLHDBC dbc, int qid) {
    SQLHSTMT stmt;
    char unit[20], qtype[20], question[MAX_QUESTION], answer[MAX_ANSWER];
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)"SELECT unit, qtype, question, answer FROM questions WHERE id = ?", SQL_NTS);
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &qid, 0, NULL);
    SQLExecute(stmt);
    
    if (SQLFetch(stmt) == SQL_SUCCESS) {
        SQLCHAR buf[512];
        SQLSMALLINT len;
        
        SQLGetData(stmt, 1, SQL_C_CHAR, unit, sizeof(unit), NULL);
        SQLGetData(stmt, 2, SQL_C_CHAR, qtype, sizeof(qtype), NULL);
        SQLGetData(stmt, 3, SQL_C_CHAR, question, sizeof(question), NULL);
        SQLGetData(stmt, 4, SQL_C_CHAR, answer, sizeof(answer), NULL);
        
        printf("\n========================================\n");
        printf("[%s] %s\n", unit, qtype);
        printf("----------------------------------------\n");
        printf("题目：%s\n", question);
        printf("========================================\n");
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

/* 记录答题结果 */
void record_result(SQLHDBC dbc, int qid, char *user_answer, int is_correct) {
    SQLHSTMT stmt;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)
        "INSERT INTO results (question_id, user_answer, is_correct) VALUES (?, ?, ?)",
        SQL_NTS);
    
    SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &qid, 0, NULL);
    SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, user_answer, 0, NULL);
    SQLBindParameter(stmt, 3, SQL_PARAM_INPUT, SQL_C_BIT, SQL_BIT, 0, 0, &is_correct, 0, NULL);
    
    SQLExecute(stmt);
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

/* 更新题目状态 */
void update_status(SQLHDBC dbc, int qid, int is_correct) {
    SQLHSTMT stmt;
    char sql[MAX_SQL];
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    
    if (is_correct) {
        /* 答对了：连续正确次数+1，如果连续2次则标记已过关 */
        sprintf(sql, 
            "UPDATE questions SET "
            "consecutive_correct = consecutive_correct + 1, "
            "wrong_count = CASE WHEN %d = 0 THEN wrong_count ELSE wrong_count END, "
            "status = CASE "
            "  WHEN consecutive_correct + 1 >= 2 THEN N'已过关' "
            "  ELSE N'待复测' END "
            "WHERE id = %d", is_correct, qid);
    } else {
        /* 答错了：错次+1，连续正确归零，状态变待复测 */
        sprintf(sql,
            "UPDATE questions SET "
            "wrong_count = wrong_count + 1, "
            "consecutive_correct = 0, "
            "status = N'待复测' "
            "WHERE id = %d", qid);
    }
    
    SQLExecDirect(stmt, (SQLCHAR*)sql, SQL_NTS);
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

/* 显示统计 */
void show_stats(SQLHDBC dbc) {
    SQLHSTMT stmt;
    SQLINTEGER total, passed, pending;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)
        "SELECT "
        "  (SELECT COUNT(*) FROM questions) AS total, "
        "  (SELECT COUNT(*) FROM questions WHERE status = N'已过关') AS passed, "
        "  (SELECT COUNT(*) FROM questions WHERE status != N'已过关') AS pending",
        SQL_NTS);
    
    if (SQLFetch(stmt) == SQL_SUCCESS) {
        SQLGetData(stmt, 1, SQL_C_SLONG, &total, 0, NULL);
        SQLGetData(stmt, 2, SQL_C_SLONG, &passed, 0, NULL);
        SQLGetData(stmt, 3, SQL_C_SLONG, &pending, 0, NULL);
        
        printf("\n===== 学习进度 =====\n");
        printf("总题数：%d\n", total);
        printf("已过关：%d\n", passed);
        printf("待复习：%d\n", pending);
        printf("====================\n");
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

/* 显示最近5条答题记录 */
void show_recent(SQLHDBC dbc) {
    SQLHSTMT stmt;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, (SQLCHAR*)
        "SELECT TOP 5 r.test_time, q.unit, q.qtype, r.user_answer, r.is_correct "
        "FROM results r JOIN questions q ON r.question_id = q.id "
        "ORDER BY r.test_time DESC",
        SQL_NTS);
    
    printf("\n最近答题记录：\n");
    while (SQLFetch(stmt) == SQL_SUCCESS) {
        char time[30], unit[20], qtype[20], ans[100];
        int correct;
        
        SQLGetData(stmt, 1, SQL_C_CHAR, time, sizeof(time), NULL);
        SQLGetData(stmt, 2, SQL_C_CHAR, unit, sizeof(unit), NULL);
        SQLGetData(stmt, 3, SQL_C_CHAR, qtype, sizeof(qtype), NULL);
        SQLGetData(stmt, 4, SQL_C_CHAR, ans, sizeof(ans), NULL);
        SQLGetData(stmt, 5, SQL_C_BIT, &correct, 0, NULL);
        
        printf("  %s | %s %s | %s | %s\n", 
               time, unit, qtype, ans, correct ? "正确" : "错误");
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

int main() {
    SQLHENV env;
    SQLHDBC dbc;
    int qid;
    char user_answer[MAX_ANSWER];
    char show_answer;
    int running = 1;
    
    srand((unsigned)time(NULL));
    
    printf("====================================\n");
    printf("   C语言 + 数据库 抽测系统\n");
    printf("   通过ODBC连接SQL Server\n");
    printf("====================================\n\n");
    
    /* 连接数据库 */
    if (!connect_db(&env, &dbc)) {
        printf("数据库连接失败，程序退出。\n");
        return 1;
    }
    
    /* 主循环 */
    while (running) {
        printf("\n操作：[Enter]抽题 | s)统计 | r)最近记录 | q)退出\n> ");
        
        char cmd = getchar();
        /* 处理换行符 */
        while (getchar() != '\n');
        
        switch (cmd) {
            case 'q':
            case 'Q':
                running = 0;
                break;
                
            case 's':
            case 'S':
                show_stats(dbc);
                break;
                
            case 'r':
            case 'R':
                show_recent(dbc);
                break;
                
            default: {
                /* 抽题 */
                qid = get_random_question(dbc);
                if (qid == 0) {
                    printf("\n全部题目已过关！恭喜！\n");
                    show_stats(dbc);
                    running = 0;
                    break;
                }
                
                show_question(dbc, qid);
                
                /* 等待用户回答 */
                printf("\n你的答案：");
                fgets(user_answer, MAX_ANSWER, stdin);
                /* 去掉换行 */
                user_answer[strcspn(user_answer, "\n")] = 0;
                
                /* 询问是否答对（演示用，实际可做自动判断） */
                printf("对照答案，你答对了吗？(y/n): ");
                show_answer = getchar();
                while (getchar() != '\n');
                
                int correct = (show_answer == 'y' || show_answer == 'Y');
                
                /* 显示正确答案 */
                SQLHSTMT stmt;
                SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
                SQLExecDirect(stmt, (SQLCHAR*)"SELECT answer FROM questions WHERE id = ?", SQL_NTS);
                SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &qid, 0, NULL);
                SQLExecute(stmt);
                if (SQLFetch(stmt) == SQL_SUCCESS) {
                    char answer[MAX_ANSWER];
                    SQLGetData(stmt, 1, SQL_C_CHAR, answer, sizeof(answer), NULL);
                    printf("正确答案：%s\n", answer);
                }
                SQLFreeHandle(SQL_HANDLE_STMT, stmt);
                
                /* 记录结果 */
                record_result(dbc, qid, user_answer, correct);
                update_status(dbc, qid, correct);
                
                if (correct) {
                    printf("答对了！继续加油！\n");
                } else {
                    printf("答错了，下次再考这道。\n");
                }
                break;
            }
        }
    }
    
    /* 断开连接 */
    SQLDisconnect(dbc);
    SQLFreeHandle(SQL_HANDLE_DBC, dbc);
    SQLFreeHandle(SQL_HANDLE_ENV, env);
    
    printf("\n再见！\n");
    return 0;
}
