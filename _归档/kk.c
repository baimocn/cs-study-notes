#include<stdio.h>
#include<math.h>
int main(){
  int n,i,flag=1;
    scanf("%d",&n);
  if(n<=1){
    printf("不是素数");
      return 0;
  }
	for(i=2;i<=sqrt(n);i++){
    if(n%i==0){
      flag=0;
      break;
    }
  }
  if(flag==1)
    printf("%d是素数\n",n);
  else
    printf("%d不是素数\n",n);
	return 0;
}