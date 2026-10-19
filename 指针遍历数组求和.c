#include <stdio.h>
int main(){
    int a[5] = {1,2,3,4,5};
    int *p;
    p = a;                     /* 第1空 */
    int sum = 0;
    for(int i=0; i<5; i++){
        sum = sum + *p;             /* 第2空 */
        p++;
    }
    printf("sum=%d\n", sum);
    return 0;
}