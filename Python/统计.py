n=input()
da=xiao=shu=0
for i in n:
    if i.isupper():
        da=da+1
    if i.islower():
        xiao=xiao+1
    if i.isdigit():
        shu=shu+1

print('da:',da,  'xiao:',xiao,  'shu:',shu)