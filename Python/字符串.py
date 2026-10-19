hua=input()
x=0
for i in hua:
    if i!=" ":
        x=x+1
    elif i=="\n":
        break
print("共有{}个字符".format(x))
HUA=hua.upper()
print(HUA)
sums=hua.split(" ")
print(sums)
tihuan=hua.replace('坏','好')
print(tihuan)