#include<stdio.h>
int main(){
    struct student{
            char name[20];
            int age;
            float score;
        };
    struct student S[3];
    for(int i=0;i<3;i++){
        scanf("%s",S[i].name);
        scanf("%d",&S[i].age);
        scanf("%f",&S[i].score);
    }
    float max=S[0].score;
    int who=0;
    for(int i=1;i<3;i++){
        if(max<S[i].score){
            max=S[i].score;
            who=i;
        }
    }
    printf("max-score=%.1f\n",max);
    printf("max-score-student=%s",S[who].name);
    return 0;



}