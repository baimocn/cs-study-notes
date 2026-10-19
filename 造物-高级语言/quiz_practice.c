/*
 * quiz_practice.c - 你来补全！
 * 
 * 这是一个抽测程序的框架，关键部分需要你填写。
 * 每个 TODO 标记的地方就是你要补的。
 * 
 * 编译：gcc quiz_practice.c -o quiz_practice.exe -lodbc32
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <sql.h>
#include <sqlext.h>

#define MAX_SQL 1024
#define MAX_ANSWER 500

/*
 * 第一关：连接数据库
 * 
 * TODO：补全连接字符串
 * 提示：Driver、Server、Database、Trusted_Connection
 */
SQLHDBC connect_db(SQLHENV *env, SQLHDBC *dbc) {
    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, env);
    SQLSetEnvAttr(*env, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    SQLAllocHandle(SQL_HANDLE_DBC, *env, dbc);
    
    SQLCHAR connStr[] = "TODO: 写出连接字符串";
    
    SQLDriverConnect(*dbc, NULL, connStr, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
    return *dbc;
}

/*
 * 第二关：查询未过关的题目数量
 * 
 * TODO：补全SQL语句
 * 提示：COUNT(*) + WHERE条件
 */
int get_count(SQLHDBC dbc) {
    SQLHSTMT stmt;
    SQLINTEGER count = 0;
    
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    SQLExecDirect(stmt, "TODO: 写出查询语句", SQL_NTS);
    
    if (SQLFetch(stmt) == SQL_SUCCESS) {
        SQLGetData(stmt, 1, SQL_C_SLONG, &count, 0, NULL);
    }
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
    return count;
}

/*
 * 第三关：插入一条答题记录
 * 
 * TODO：补全INSERT语句和参数绑定
 * 参数：question_id, user_answer, is_correct
 */
void record_result(SQLHDBC dbc, int qid, char *answer, int correct) {
    SQLHSTMT stmt;
    SQLAllocHandle(SQL_HANDLE_STMT, dbc, &stmt);
    
    SQLExecDirect(stmt, "TODO: 写出INSERT语句", SQL_NTS);
    
    // TODO: 绑定参数（提示：SQLBindParameter）
    
    SQLExecute(stmt);
    SQLFreeHandle(SQL_HANDLE_STMT, stmt);
}

int main() {
    SQLHENV env;
    SQLHDBC dbc;
    char answer[MAX_ANSWER];
    
    printf("=== 抽测系统 ===\n\n");
    
    // 连接数据库
    connect_db(&env, &dbc);
    
    // 显示还有多少题没过
    int remaining = get_count(dbc);
    printf("还有 %d 题待复习\n\n", remaining);
    
    // TODO: 你来设计后面的流程
    // 思考：怎么抽题？怎么显示？怎么判断对错？
    
    // 断开连接
    SQLDisconnect(dbc);
    SQLFreeHandle(SQL_HANDLE_DBC, dbc);
    SQLFreeHandle(SQL_HANDLE_ENV, env);
    
    return 0;
}
