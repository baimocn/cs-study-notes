#include <stdio.h>
int main(){
    int count = 0;
    char ch;
    while((ch = getchar()) !='#'){    /* 第1空 */
        if(ch >= '0' && ch<='9'){   /* 第2空 */
            count++;
        }
    }
    printf("数字个数=%d\n", count);
    return 0;
}