#include<stdio.h>
int main(){
    int n=5;
    int *p;
    p=&n;
    printf("%d\n",*p);
    printf("%p\n",p);
    printf("%d\n",n);
    printf("%p\n",&n);
    return 0;
}