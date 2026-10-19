#include<stdio.h>
int main(){
    int a[5]={10,20,30,40,50};
    int *p=a;
    printf("%d\n",p[2]);
    printf("%d\n",*(p+2));
    printf("%d\n",a[2]);
    printf("%d\n",*(a+2));
    return 0;
}