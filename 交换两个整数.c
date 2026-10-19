#include <stdio.h>
void swap(int *a,int *b){              /* 第1空 */
    int t = *a;
    *a = *b;
    *b = t;
}
int main(){
    int x = 3, y = 8;
    swap(&x,&y);                         /* 第2空 */
    printf("x=%d y=%d\n", x, y);
    return 0;
}