#include<stdio.h>
#define square(x) ((x)*(x))
#define pi 3.14159
#define max(a,b) ((a)>(b)?(a):(b))
int main(){
    float n;
    scanf("%f",&n);
    float m;
    scanf("%f",&m);
    float nn=square(n);
    float mm=square(m);
    float da=max(n,m);
    printf("%f\n",pi);
    printf("%f\n",nn);
    printf("%f\n",mm);
    printf("%f\n",da);
    return 0;
}