# C8-文件 候选池（candidates.md）
来源：《高级语言程序设计（2017年版）》郑岩 ch10（教材页 309-335）。OCR 严重劣化，坏字见 verified.md 附表。

## 池1：概念/定义池
- C1-01 流式文件：C 把文件看作字符（ASCII 文件）或字节（二进制文件）序列；其他高级语言以记录为单位。（P309）
- C1-02 文件定义：存储在外部存储介质上的数据集合；磁盘上的称"磁盘文件"。
- C1-03 文件名组成：盘符:路径\文件主名[.扩展名]；路径出现在字符串中时 `\` 必须写成 `\\`。盘符/路径可省略→当前盘/当前路径。（P309）
- C1-04 常见扩展名：.c 源程序、.obj 目标文件、.exe 可执行文件；数据文件常用 .dat，文本文件常用 .txt。
- C1-05 文件四角度分类：①内容：程序文件（源/目标/可执行）与数据文件；②组织形式：顺序存取文件（长度可不同、从头查）与随机存取文件（定长、按编号公式定位）；③存储形式：文本文件（转 ASCII，逐字符，占空间多、有转换时间）与二进制文件（内存原样输出，省空间省时间，不能直接输出字符形式）；④存储介质：普通文件与设备文件。（P310）
- C1-06 int a=10000 的存储：文本=5 个 ASCII 字符字节；二进制=内存原样（如 4 字节）。教材图10-1。
- C1-07 缓冲文件系统（标准 I/O）：系统自动为每个文件开辟内存缓冲区，装满才成批传输；ANSI C 只采用缓冲文件系统。（P311）
- C1-08 读文件=磁盘→内存；写文件=内存→磁盘。
- C1-09 FILE 类型：特殊结构体，成员存放缓冲区位置/大小、当前读写位置、读写状态、是否到文件尾等；由 stdio.h 定义，类型名 FILE 必须大写。文件型指针定义：FILE *fp;
- C1-10 打开时系统自动建立文件结构体并返回指针；关闭时释放。
- C1-11 三种标准设备文件：stdin（键盘）、stdout（显示器）、stderr（显示器）；系统自动打开、退出时自动关闭，不必也不应 fclose。（P314，表10-3）

## 池2：函数/对偶池（主钩子素材）
- C2-01 fopen(filename, mode)：成功返回 FILE*，失败返回 NULL（stdio.h 中定义、值为 0）。mode 由 r/w/a/t/b/+ 组成；含 b→二进制，不含 b→文本（t 可省略）；"r" 打开时文件必须已存在。
- C2-02 六模式串口诀素材（表10-2）：r 只读（文件必须存在）；w 只写（存在则清空重建，不存在则创建）；a 追加（写到文件尾，文件不存在则创建）；每者可加 + 变读/写；每者可加 b 变二进制 → r r+ / w w+ / a a+ / rb rb+ / wb wb+ / ab ab+ 共 12 串。
- C2-03 exit(状态值)：关闭所有已打开文件并结束程序返回操作系统；0 正常，非 0 出错；头 stdlib.h（教材正文一处写 stdio.h，附录函数表未列头文件，按 C 标准为 stdlib.h）。
- C2-04 fclose(fp)：关闭文件并释放缓冲区；成功返回 0，否则非 0。
- C2-05 feof(fp)：遇文件尾返回非 0，否则返回 0；文本/二进制通用；二进制文件判文件尾必须用 feof；文本文件还可判 EOF（符号常量，值为 -1）。
- C2-06 【对偶一】fputc(ch, fp) 写一字符（返回该字符，错则 EOF）↔ fgetc(fp) 读一字符（返回该字符，错/尾则 EOF）。读写后位置指针均自动后移 1 字节。
- C2-07 【对偶二】fputs(str, fp) 写字符串（舍去 '\0'，指针后移 strlen 字节；返回实际字符数，错则 EOF）↔ fgets(str, length, fp) 读字符串（读 length-1 个字符并自动补 '\0'；遇 EOF 或回车提前结束；成功返回 str 地址，失败返回 NULL）。
- C2-08 puts vs fputs：puts 把 '\0' 转换为 '\n' 输出；fputs 舍去 '\0' 不换行。gets vs fgets：gets 把回车换成 '\0'；fgets 保留回车再补 '\0'。
- C2-09 【对偶三】fwrite(buffer, size, count, fp) 写数据块（返回 count，错则 0）↔ fread(buffer, size, count, fp) 读数据块（返回 count）。size 常用 sizeof(类型)；位置指针后移 size×count 字节；一般用于二进制文件。
- C2-10 【对偶四】fprintf(fp, format, …) 格式化写（返回输出字符个数，错则负）↔ fscanf(fp, format, …) 格式化读（返回读入数据个数，错则 EOF）。与 printf/scanf 唯一区别：多一个文件型指针且在参数表最前。
- C2-11 rewind(fp)：位置指针重置到文件头；成功返回 0。
- C2-12 fseek(fp, offset, origin)：offset 长整型位移量（正后/负前），常数须加 L；origin 三取值：0=SEEK_SET 文件头、1=SEEK_CUR 当前位置、2=SEEK_END 文件尾；成功返回 0；一般用于二进制文件。
- C2-13 文件位置指针本质：FILE 成员，不是真指针，是"下一次读写字节位置"的整数值；每次读写自动后移。

## 池3：例题池
- C3-01 例10-1 打开文件标准程序段：if((fp=fopen("文件名","使用方式"))==NULL){printf("cannot open this file\n");exit(1);} —— 赋值表达式值判 NULL。
- C3-02 例10-4 从键盘输入字符逐一写入 f:\g.txt（"w"），输入 # 结束；f:\\ 转义。
- C3-03 例10-5 文件复制：源 "r" + 目标 "w"，while((ch=fgetc(fpr))!=EOF) fputc(ch,fpw); —— 本单元最典型完整流程。
- C3-04 例10-6 fgets 逐行读文本加行号显示：while(fgets(ch,SIZE,fp)!=NULL) printf("%4d\t%s",line++,ch)。
- C3-05 例10-7 fputs 写 / fgets 读 + fputs(string2, stdout) 把标准设备当文件用。
- C3-06 例10-8 fwrite/fread 结构体数组存取二进制文件 stu_list（"wb"/"rb"）。
- C3-07 例10-9 fprintf/fscanf 改写例10-8（每次只能读写一个元素，须循环）。
- C3-08 例10-10 rewind 例：文件先显示再复制到另一文件（读两遍，中间 rewind）。
- C3-09 例10-11 fseek 三句示例：fseek(fp,-2L,1); fseek(fp,5L,SEEK_SET); fseek(fp,-6L,SEEK_END)。
- C3-10 例10-12 随机读 stud.dat 第 2,4,6,8,10 名（fseek 定位+循环）+ SEEK_END 前移 2×sizeof 读第 9 名。
- C3-11 例10-13 随机写账户 client.dat（"rb+"），fseek((acctNum-1)*sizeof(...), SEEK_SET) + fwrite。
- C3-12 习题程序分析 6 道可改编为"读程序写结果"：w 清空重写+rewind 回读、fseek(-3L,SEEK_END) 取倒数第 3 字节、w+n 格式写后 rewind 格式读、fputs 追加、fread 参数顺序辨析等。

## 池4：题型池
- C4-01 单选：文件由字符（字节）序列组成（流式文件）。
- C4-02 单选：标准输入文件=键盘 stdin。
- C4-03 单选：读写完毕必须关闭，否则可能数据丢失（选D）；A 错在 w 才覆盖而 a 不覆盖、C 错在流式文件也可随机存取。
- C4-04 单选：修改非空文件应选 "r+"（w 清空、a 只能尾追、a+ 尾追）。
- C4-05 单选：fopen("C:\\user\\test.txt","r+") 路径转义 + 读写模式。
- C4-06 单选："r+" 打开已存在文件：内容不删、指针到文件头、可重写可读。
- C4-07 单选：fscanf 正确调用形式=文件指针在首。
- C4-08 单选："w" 方式只能写不能读。
- C4-09 单选：rewind() 不能用于写数据；fputc 成功返回"输出的字符"本身。
- C4-10 单选：fread(buf, size, count, fp) 读 size×count 字节到 buf。
- C4-11 单选：fseek(fp,-20L,2)=从文件尾前移 20 字节。
- C4-12 单选：fseek(fp,0L,SEEK_SET) 等价 rewind(fp)。
- C4-13 填空：文件操作三步=打开、读/写、关闭。
- C4-14 填空：文本文件/二进制文件；顺序存取/随机存取；文件型指针（FILE *fp; + #include<stdio.h>）。
- C4-15 填空：新二进制文件只写 → "wb"；fscanf 成功返回读入数据个数，否则 EOF；fclose 同时释放缓冲区；feof 功能。
- C4-16 程序分析：w 清空重写→rewind→回读（输出重写后的串）。
- C4-17 程序分析：fseek(fp,-3L*sizeof(char),SEEK_END)+fread → 输出倒数第 3 个字符。
- C4-18 程序分析：fprintf 写 + rewind + fscanf 回读（注意 %d 之间空格/无分隔符的边界）。
- C4-19 程序填空：fopen 模式串、fgetc 判 #、fgets/fputs 参数、fread/fwrite 参数补全、fscanf/fprintf 参数补全。
- C4-20 简答/对比：文本 vs 二进制差异；fputs vs puts 差异；顺序 vs 随机存取。
- C4-21 程序设计：素数存文件、两文件合并、学生成绩排序存盘、员工信息筛选存盘。

## 池5：边界/坑池
- C5-01 "w" 会删去原文件全部内容再写；"a" 才是保留原内容尾部追加。教材 P328 单选3 的 A 项就是拿"写操作必覆盖"做干扰。
- C5-02 "r"（含 r+、rb、rb+）打开时文件必须已存在，否则 fopen 返回 NULL；w/a 不存在则自动创建。
- C5-03 路径中的 \ 在字符串里必须写 \\（例10-4 的 f:\\g.txt、例10-10 的 d:\\fengyi\\bkc\\ch1.c）。
- C5-04 判文件尾：二进制必须 feof(fp)；文本可用 fgetc 返回 EOF 判。EOF 值为 -1，是符号常量不是函数。
- C5-05 fgets 读 n-1 个字符自动补 '\0'，且遇到回车会连回车一起保留——回读字符串常带 '\n'，这是它与 puts 输出差一行的根源。
- C5-06 fputs 舍去 '\0' 不自动换行；想换行须自己写 '\n' 或用 puts。
- C5-07 fscanf/fprintf 的文件型指针在参数表第一位； scanf/printf 没有这一位——参数顺序是高频考点。
- C5-08 fread/fwrite 参数顺序 buffer,size,count,fp；返回成功个数 count，判错比较对象是 count 不是 0（写时错才 0）。
- C5-09 fseek 位移量必须是 long：常数加 L（-2L、5L），表达式用 (long) 强转；origin 用 0/1/2 或 SEEK_SET/SEEK_CUR/SEEK_END。
- C5-10 fclose 不只"关门"：释放缓冲区；不 fclose 可能丢数据（缓冲区未满未刷盘）——教材 P312 与单选3 D 项。
- C5-11 stdin/stdout/stderr 自动开关，不要对它们 fopen/fclose。
- C5-12 fopen 返回值判 NULL 的标准写法是赋值表达式整体比较：if((fp=fopen(...))==NULL)。
- C5-13 "w+" 打开已存在文件同样先清空（教材表10-2 原文）；想读旧内容又要写只能 r+ 或 a+。
- C5-14 文本模式下写入的 '\n' 在 Windows 磁盘上是 '\r\n' 两字节，回读按文本模式又转回——用二进制方式算位移时这是坑（教材讲文本/二进制换行行为差异的落点，见 verified.md 核验注记）。
