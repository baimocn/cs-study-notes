#include<string.h>
#include<stdio.h>
char s[]="hello";
char *p=s;
int main(){
    while(*p!='\0'){
        printf("%c ",*(p++));
    }
    printf("len=%d",strlen(s));
    return 0;

}