#include<stdio.h>
void swap(int *a,int *b){
    int temp=*a;
    *a=*b;
    *b=temp;
}
int main(){
    int x=3;
    int y=8;
    swap(&x,&y);
    printf("x=%d,y=%d",x,y);
    return 0;

    
} 