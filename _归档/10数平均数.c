#include<stdio.h>
double average(double *x,double *y){
    return *y=*x/10;
}
int main(){
    double sum=0,avg,su;
    int i;
    for(i=1;i<=10;i++){
        scanf("%lf",&su);
        sum=sum+su;
    }
    average(&sum,&avg);
    printf("avg=%lf\n",avg);
    return 0;
}