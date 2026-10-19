with open("score.txt","w") as f:
    f.write("张三 90\n")
    f.write("李四 85\n")
    f.write("王五 78\n")
with open("score.txt","r") as f:
    content=f.read()
    print(content)
with open("score.txt","a") as f:
    f.write("赵六 92\n")
with open("score.txt","r") as f:
    conten=f.read()
    print(conten)