#include <stdio.h>
//函数//
void ji_ou(int *x){
    if(*x%2==0){
    printf("%d是偶数\n",*x);  
    }
    else{
    printf("%d是奇数\n",*x);
    }
}
void hege(int *x){
    if(*x>=60){
        printf("%d及格了\n",*x);
    }
    else{
        printf("%d不及格\n",*x);
    }
}
//数组//
int main(){
    printf("input 10 scores:\n");
    int score[10];
    for(int i=0;i<10;i++){
        scanf("%d",&score[i]);
    }
    int max=score[0];
    for(int a=1;a<10;a++){
        if(score[a]>max){
            max=score[a];
        }
        
    }
    printf("max=%d\n",max);
    //条件判断//
    for(int i=0;i<10;i++){
        ji_ou(&score[i]);
        hege(&score[i]);

    }



}