#include<stdio.h>
int main(){
    FILE *fp =fopen("data.txt","r");
    if(fp==NULL){
        printf("未找到该文件\n");
        return 1;
    }
    char buf[100];
    while(fgets(buf,100,fp)!=NULL){
        printf("%s",buf);
    }
    fclose(fp);
    return 0;
    
}