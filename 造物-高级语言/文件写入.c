#include<stdio.h>
int main(){
    struct student{
        char name[20];
        int age;
        float score;
    };
    struct student s[3];
    for(int i=0;i<3;i++){
        scanf("%s",s[i].name);
        scanf("%d",&s[i].age);
        scanf("%f",&s[i].score);
    }
    FILE *fp = fopen("data.txt","w");
    if(fp==NULL){
        printf("open-fail\n");
        return 1;
    }
        for(int z=0;z<3;z++){
            fprintf(fp,"%s ",s[z].name);
            fprintf(fp,"%d ",s[z].age);
            fprintf(fp,"%.1f\n",s[z].score);
        }
    fclose(fp);
    return 0;

}

