#include<stdio.h>
int main(){
    int n;
    int flg=1;
    scanf("%d",&n);
    if(n<=1){
            printf("%d不是素数\n",n);
            return 0;
        }
    
    for(int i=2;(i*i)<=n;i++){
        
        if(n%i==0){
            flg=0;
        }
    }
    if(flg==0){
        printf("%d不是素数\n",n);
    }
    else{
        printf("%d是素数\n",n);
    }
    return 0;

}
