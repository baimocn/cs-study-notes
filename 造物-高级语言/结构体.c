#include<stdio.h>
int main(){
    struct student{
        char name[20];
        int age;
        float score;
    };
    struct student S1;
    scanf("%s",&S1.name);
    scanf("%d",&S1.age);
    scanf("%f",&S1.score);
    printf("姓名=%s ",S1.name);
    printf("年龄=%d ",S1.age);
    printf("成绩=%f ",S1.score);
    return 0;
}