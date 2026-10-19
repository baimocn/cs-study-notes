#include<stdio.h>
int findMax(int *arr,int n){
    int max=arr[0];
    for(int i=1;i<n;i++){
        if(max<arr[i]){
            max=arr[i];
        }
    }
    return max;
}
int main(){
    int a;
    printf("请输入数组长度:");
    scanf("%d",&a);
    int bnn[a];
    printf("请输入%d个数值:\n",a);
    for(int i=0;i<a;i++){
        scanf("%d",&bnn[i]);
    }
    int max=findMax(bnn,a);
    printf("最大值是：%d",max);
    return 0;


}