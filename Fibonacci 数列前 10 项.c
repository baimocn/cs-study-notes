#include <stdio.h>
int main(){
    int a[10] = {1,1};
    for(int i=2; i<10; i++){
        a[i] = a[i-2]+a[i-1];      /* 第1空 */
    }
    for(int i=0; i<10; i++){
        printf("%d ",a[i]);  /* 第2空 */
    }
    return 0;
}