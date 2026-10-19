n=eval(input())
if n<=1:
    print(n,'不是素数',sep='')
else:
 temp=0
 for i in range(2,n):
    if n%i==0:
        temp=1
 if temp==1:
    print(n,'不是素数',sep='')
 else:
    print(n,'是素数',sep='')
