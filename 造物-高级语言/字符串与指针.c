#include<stdio.h>
#include<string.h>
int main(){
    char s[]="hello";
    char *p=s;
    for(int i=0;i<strlen(s);i++){
        printf("%c ",*(p+i));
    }
    printf("\n");
    printf("len=%d",strlen(s));
    return 0;
}