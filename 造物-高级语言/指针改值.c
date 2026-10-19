#include<stdio.h>
int main(){
    int n=10;
    int *p;
    p=&n;
    *p=20;
    printf("%d\n",n);
    return 0;

}