---
name: C8-文件
description: 自考《高级语言程序设计》文件单元的考试蒸馏。覆盖：FILE*文件指针、fopen六模式串（r/w/a×+×b）、fclose、EOF与feof判据、四组读写对偶（fputc/fgetc、fputs/fgets、fwrite/fread、fprintf/fscanf）、rewind与fseek定位、文本vs二进制差异。核心钩子=读写对偶表（会一个等于会两个）+六模式口诀。题型：模式串选择、fseek位置计算填空、读程序写结果、文本vs二进制简答。
source_book: 《高级语言程序设计（2017年版）》郑岩
source_chapter: ch10
---

# C8-文件

## R·原文修复
本节 OCR 坏字密集，统一修法：`fbpen / £叩©口 / &^。口` 读作 **fopen**；`Sutc / 4)uts / 顼枇 / 母向氓电` 读作 **fputc / fputs**；`£且©8 / £80双 / 鱼式$` 读作 **fgetc / fgets / gets**；`feeek / fceek / £$66及电` 读作 **fseek**；`近让 / 《乂让` 读作 **exit**；`F止E / HLE / FH,E / FE,E` 读作 **FILE**；返回值处的 `瓯匕 / £€^ / 诋1` 读作 **NULL / EOF**。表10-1 中 w 的含义"5"应为"**写**"；"标准 DO / 系统 V 0"应为"**标准 I/O / 系统 I/O**"；盘符"人、B、€：和口"即"A、B、C 和 D"。例10-12 循环条件 `i*=2` 与题面"第2、4、6、8、9、10名"对不上（教材自身粗疏）：按"fseek 按序号×sizeof 定位"理解考点，不复现该循环。

## I·骨架与钩子
文件操作的骨架只有三步：**打开（fopen）→ 读写（配对函数）→ 关闭（fclose）**。其余全是往这三步里填东西。

> **钩子1·对偶表（本单元主钩子）**：读写函数天生成对，会一个等于会两个——
>
> | 读 | 写 | 单位 | 典型文件 |
> |---|---|---|---|
> | fgetc(fp) | fputc(ch,fp) | 1 字符 | 文本 |
> | fgets(str,n,fp) | fputs(str,fp) | 1 串 | 文本 |
> | fread(buf,size,count,fp) | fwrite(buf,size,count,fp) | 数据块 | 二进制 |
> | fscanf(fp,格式,…) | fprintf(fp,格式,…) | 格式化 | 两者 |
>
> 骨架口诀：**中间是干什么的，前面给地址，最后给 fp**；唯独 fscanf/fprintf 的 fp 排**第一位**。
> 对偶互证：fputc 成功返回**刚写入的字符**，失败 EOF；fgetc 成功返回读到字符，失败/到尾 EOF——返回值也成对。

> **钩子2·六模式口诀**："**读 r 写 w 添 a 追加，加 + 能读写，加 b 变二进制**"。r/w/a 各可配 `+`（变读/写）和 `b`（变二进制）。三个模式互踩：**r** 文件必须已存在；**w** 存在则**清空重来**；**a** 保留原内容**尾巴接着写**。不加 b 默认文本文件（t 可省略）。

12 串速查（文本 6 串，加 b 是二进制镜像）：

| 模式 | 语义 | 文件不存在时 |
|---|---|---|
| r | 只读，指针在头 | 报错（返回 NULL） |
| r+ | 读/写，指针在头，**不删内容** | 报错（返回 NULL） |
| w | 只写，**清空**原内容 | 自动创建 |
| w+ | 读/写，**清空**原内容 | 自动创建 |
| a | 只写，**追加**到尾 | 自动创建 |
| a+ | 读/写，写**追加**到尾 | 自动创建 |

> **钩子3·fseek 起点三兄弟**："**头 0、腹 1、尾 2**"——0=SEEK_SET 文件头，1=SEEK_CUR 当前位置，2=SEEK_END 文件尾。位移量是 long：常数要写 `-2L`、`5L`，表达式要 `(long)` 强转。

概念底座（填空高频）：
- C 文件是**流式文件**——字符（文本）/字节（二进制）序列，不是记录序列。
- 文本文件按 ASCII 存（占空间多、要转换）；二进制按内存原样存（省空间省时间、不能直接显示）。例：int a=10000，文本=5 个 ASCII 字节，二进制=内存原样。
- ANSI C 只用**缓冲文件系统**：缓冲区没满不落盘——所以**必须 fclose**，否则可能丢数据。
- 三个标准设备文件 stdin（键盘）/stdout（显示器）/stderr（显示器）系统自动开、自动关，**不用 fclose**。
- 文件位置指针不是真指针，是 FILE 结构体成员里"下一次读写字节位置"的整数值，每次读写自动后移；存取两分：顺序存取（常配文本）与随机存取（fseek，常配二进制）。

## A1·书中例题完整流程（例10-5 文件复制）
```c
#include <stdio.h>
#include <stdlib.h>
int main(void)
{
    char ch, rfile[20], wfile[20];
    FILE *fpr, *fpw;                       /* ① 定义文件型指针 */
    printf("Please input the source filename:\n");
    gets(rfile);
    printf("Please input the destination filename:\n");
    gets(wfile);
    if ((fpr = fopen(rfile, "r")) == NULL) /* ② 打开源文件：只读，判NULL */
    { printf("Cannot open the file\n"); exit(1); }
    if ((fpw = fopen(wfile, "w")) == NULL) /* ② 打开目标文件：只写，判NULL */
    { printf("Cannot open the file\n"); exit(1); }
    while ((ch = fgetc(fpr)) != EOF)       /* ③ 逐字符读源文件，EOF即停 */
        fputc(ch, fpw);                    /*    读一个写一个（对偶互咬） */
    fclose(fpr);                           /* ④ 关闭：释放缓冲区，防丢数据 */
    fclose(fpw);
    return 0;
}
```
流程四判：打开判 NULL → 源"r"目标"w" → fgetc/fputc 对偶搬运 → 双 fclose。exit(1) 顺带关闭所有已打开文件。

**同族例·例10-10（rewind 用法）**：显示文件内容并复制到另一文件——`while(!feof(fp1)) putchar(fgetc(fp1));` 显示一遍后，`rewind(fp1);` 拨回文件头，再 `while(!feof(fp1)) fputc(fgetc(fp1),fp2);` 复制一遍。顺序读写到尾后指针停在 EOF，想再读必须 rewind（或 fseek 归零）——这是 rewind 的唯一考点。

**数据块对偶要点（例10-8/9 压缩）**：`fp=fopen("c:\\stu_list","wb"); fwrite(stud,sizeof(struct student_type),4,fp); fclose(fp);` 再 `"rb"` 打开 `fread(stud,sizeof(...),4,fp)` 整块读回。size 用 `sizeof(类型)`；判错看返回个数是否等于 count。fprintf/fscanf 版（例10-9）同结构，换成 `fprintf(fp,"%s %d %d %s\n",...)` / `fscanf(fp,"%s%d%d%s",...)`——教材注明每次只能处理一个元素，必须循环。

## A2·触发题型★
1. 填空（模式串选择）：若用 fopen() 打开一个**新的**二进制文件，要求**只能写入**，使用方式字符串应为 `______`。（答：`"wb"`——新文件→w；二进制→b；只写→不带 +）
2. 填空（fseek 三选一）：`fseek(fp, -20L, ______)` 表示位置指针从**文件尾**前移 20 字节。（答：`2` 或 `SEEK_END`；若写 `fseek(fp,20L,2)` 则是从文件尾**后**移，出界非法）
3. 填空：文件操作三步 = 打开、读/写、______；EOF 的值为 ______；fscanf 成功返回 ______，失败返回 ______。（答：关闭；-1；读入的数据个数；EOF）
4. 单选：修改一个非空文件应选哪种方式？`"w"` 清空 ✗，`"a"`/`"a+"` 只能尾追 ✗，`"r+"` 不删内容、指针在头、可读可写 ✓。
5. 读程序写结果：`"w"` 打开→写入"welcome"→fclose→`"a"` 再打开→fprintf 追加"55"→`rewind`→fscanf 读 `%s` →输出 `welcome55`（追加不删原内容；rewind 后从头读）。
6. 读程序写结果：char a[4]="abcd" 以 "wb" 写入，再 "rb" 打开，`fseek(fp,-3L*sizeof(char),SEEK_END); fread(&b,sizeof(char),1,fp);` → 输出 `b`（文件尾前移 3 字节 = 4 个字符中倒数第 3 个）。
7. 简答（文本 vs 二进制）：文本文件逐字节存 ASCII、可直接显示、占空间多、有转换开销；二进制按内存原样存、省空间省转换、不能直接输出字符形式、判文件尾必须用 feof()。
8. 单选（fopen 路径+模式）：打开 C 盘 user 子目录下 test.txt 进行读/写，正确的是 `fopen("C:\\user\\test.txt","r+")` ✓；`"C:\user\..."` 未转义 ✗、`"r"` 不能写 ✗、`"w"` 清空 ✗。
9. 单选（fseek 语义）：`fseek(fp,-20L,2)` = 从文件尾前移 20 字节 ✓；"从当前位置后移 20 字节"是 `fseek(fp,20L,1)`。
10. 单选（函数辨析）：不能向文件写数据的是 rewind()（只拨指针）；fputc 成功返回**输出的字符本身**，不是 1。

## E·考场步骤
拿到文件题，先在心里过这四问，再动笔：

**文件题四步判**：
1. **打开**：fopen 两参（文件名字符串、模式串）——路径 `\` 必写 `\\`；返回值与 NULL 比较。
2. **判模式**：口诀"读 r 写 w 添 a 追加，加 + 能读写，加 b 变二进制"；r 必须已存在、w 清空、a 追加。
3. **读写啥配啥**：
   - 读字符↔写字符（fgetc/fputc）：文本文件判 EOF，二进制判 `feof(fp)`（返回非0=到尾）。
   - 读串↔写串（fgets/fputs）：fgets 最多读 n-1 个字符补 '\0'，判 NULL。
   - 数据块↔数据块（fread/fwrite）：判返回的**成功个数**是否等于 count。
   - 格式化（fscanf/fprintf）：**fp 在第一位**，其余同 scanf/printf。
4. **关闭**：fclose(fp) 返回 0=成功；关了才刷缓冲区。

标准读循环模板（判尾两法）：
```c
while ((ch = fgetc(fp)) != EOF)  { ... }  /* 文本文件：EOF=-1 */
while (!feof(fp))                { ... }  /* 通用，二进制必须用这个 */
```

**fseek 起点判据**：题目说"从文件头"→ 0/SEEK_SET；"从当前位置"→ 1/SEEK_CUR；"从文件尾"→ 2/SEEK_END。最终位置 = 起点偏移 + 位移量：如 `fseek(fp,-20L,2)` = 距文件头 文件长-20 字节处。等价关系：`fseek(fp,0L,SEEK_SET)` ≡ `rewind(fp)`。随机定位读写套路：`fseek(fp,(序号-1)*sizeof(类型),0); fread(&x,sizeof(类型),1,fp);`

**程序分析题秒杀链**（真题最常考的组合拳）：
1. 第一段 fopen 用了 `w`/`w+`？→ 不管文件原来有什么，内容被清空，之前写的全作废。
2. 写完没关闭又用 `a`/`a+`/`r+` 重新打开？→ 内容保留，指针位置决定从哪读：`a+` 指针在尾（读需先 rewind/fseek），`r+` 指针在头。
3. 中间有没有 `rewind`？→ 没有则第二次读从上次停下的位置继续（多半读不到想要的数据）。
4. 读回时 fscanf/fgets 的格式与写入格式对不对齐？→ fprintf 写 `%d` 不带分隔符连写两个，fscanf 按 `%d` 读会粘连出错。
5. fseek 负位移+SEEK_END？→ 换算成"倒数第 n 个元素"：`-n*sizeof(类型)` 即倒数第 n 个。

**程序填空题高频空位**（对照 A1/A2 例背空）：空 fopen 第二参（"二进制/文本+只读/只写/追加/读写"四选一）；空判尾 `while(!feof(fp))` 或 `while((ch=fgetc(fp))!='#')`；空 fread/fwrite 中间两参 `sizeof(类型),个数`；空 fseek 起点参 0/1/2；空收尾 fclose。

## B·边界★
**失分点**：
- **"w" 清空 vs "a" 追加**：w 删原文件全部内容后重写；a 保留原内容在尾部追加。见"写操作"就选 w = 送分变送命。单选3 的 A 项"写操作后原有数据必定被覆盖"错就错在 a 不覆盖。
- **文本 vs 二进制的读回陷阱**：写文本用文本模式、读二进制数据用二进制模式，模式串配错则数字读回全乱；同一数据两种格式互不兼容（10000：文本 5 字节 ASCII vs 二进制原样字节）。
- **fclose 漏刷写缓存**：缓冲文件系统下数据先存内存缓冲区，未满不落盘；不 fclose 就退出 → 尾部数据丢失，且缓冲区不释放。教材原话："使用结束后应立即关闭，以免数据丢失"。
- **位移量忘写 L**：教材要求长整型——`-20L`；表达式要 `(long)` 强转。
- **参数序**：fread/fwrite 是 buffer,size,count,fp；fscanf/fprintf 是 **fp 在最前**——两个家族顺序完全不同。
- **判 NULL 书写**：标准写法是赋值表达式整体比较 `if((fp=fopen(...))==NULL)`；写成 `if(fp=fopen(...))` 逻辑反了还丢判据。
- **stdin/stdout/stderr 不许 fopen/fclose**：系统自动管理，只可当现成 fp 用（如 fputs(s,stdout)）。
- **返回值别记反**：fclose 成功返回 **0**、失败非 0；feof 到尾返回**非 0**、未到尾返回 0；`"w+"` 也清空（+ 只合并读写权限，不清空豁免）；EOF 是符号常量（-1）不是函数。

**跨单元混淆表**：

| 本单元 | 易混单元 | 分界 |
|---|---|---|
| fgets(str,n,fp) 从文件读串，遇到回车**保留**'\n'再补'\0' | C3 gets(s) 从键盘读串，回车换成'\0' | 一个读文件一个读键盘；fgets 的字符数组底盘来自 C3，判空判溢规则沿用 C3 |
| fputs(str,fp) 写文件，舍去'\0'不换行 | puts(s) 输出时把'\0'换成'\n' | fputs 后想要换行须自己 fputc('\n',fp)；puts 自带换行 |
| FILE* fp 是指向文件结构体的指针，只作 fopen/fclose/读写函数的参数 | C5 字符串指针 char *p 指向字符，可 p++ 逐字符走 | 文件指针不自增，位置移动交给 fgetc/fseek；别把 fp 当字符串指针传给 strlen/strcpy |

**延伸一句**：章末程序设计题（素数存盘、两文件合并、排序存盘）= 四步判+循环+对偶搬运，无新知识。
## 审计
- 行数：149 行（物理行，含 frontmatter），在 110-150 区间 ✅
- frontmatter：name=C8-文件；description=224 字 ≤300；source_book/source_chapter 齐 ✅
- 钩子：对偶表为主钩（四行四对，读写两侧一成一列无缺席列），六模式口诀、fseek 三兄弟为副钩 ✅
- A1 = 教材例10-5 完整四步流程 + 例10-10 rewind 同族例 + 例10-8/9 数据块要点 ✅
- A2 十题：模式串填空、fseek 填空、返回值填空、单选×4、读程序写结果×2、简答 ✅
- E = 四步判 + 判尾两法模板 + fseek 判据 + 秒杀链 + 填空空位 ✅
- B 边界：w 清空/读回陷阱/fclose 刷缓存/参数序/跨单元混淆表（C3 fgets、C5 文件指针）✅
- 淘汰留痕见 verified.md；OCR 坏字修法见 R 节 ✅
