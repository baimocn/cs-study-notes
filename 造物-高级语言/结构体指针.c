#include<stdio.h>
struct student{
    char name[20];
    int age;
    float score;
};
int main(){
    struct student s;
    scanf("%s",s.name);
    scanf("%d",&s.age);
    scanf("%f",&s.score);
    struct student *p = &s;
    printf("%s ",p->name); 
    printf("%d ",p->age);
    printf("%.1f ",p->score);
    return 0;
}