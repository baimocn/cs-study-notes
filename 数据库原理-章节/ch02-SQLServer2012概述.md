# 第2章 SQL Server 2012 概述

SQL Server 是 Microsoft 公司推出的关系型数据库管理系统，是一个全面的数据库平 (BI) 提供了企业级的数据管理，具有使用方便、可伸缩 台，它使用集成的商业智能工具 性好、与相关软件集成度高等特点。娄 数据引擎为关系型数据和结构化数据提供了安全可靠 的存储，可构建并管理用于业务的高性能数据应用程序。 延续 SQL Server 2008 的构架，SQL Server 2012 属于 C/S 模式 (Client/ Server 模式, 即客户端/服务器模式）的大型分布式关系型数据库管理系统。它延续了现有数据平台的强 大能力，对数据库中的数据提供有效的管理，并有效实现数据的完整性和安全性，且全面 支持云技术，为数据管理提供了强大的支持，是电子商务、数据仓库和数据解决方案等应 用中的核心。

## SQL Server 2012 概述

### 2.1

SQL Server 2012 在 SQL Server 2008 基础上进行了提升，提供了一个全面、灵活、可 扩展的数据仓库管理平台，以满足众多用户的海量数据管理需求，能快速构建相应的解决 方案实现私有云与公有云之间数据的扩展与应用的迁移。 SQL Server 2012 与微软公司的 Windows 操作系统高度集成，能最充分地利用视窗操 作系统的优势。其数据引擎是企业数据管理解决方案的核心，结合了分析、报表、集成和 通知等功能，可以构建和部署经济有效的集成商业智能解决方案。通过与 Microsoft Visual Studio、Microsoft Office System 以及新的开发工具包（包括Business Intelligence Development 的紧密结合使 SQL Server 2012 成为众多数据库用户的第一选择。SQL Server 2012 Studio） 在基于 SQL Server 2008 的强大功能之上，提供了一个完整的数据管理和分析的解决方案, 可用于大型联机事务处理、数据仓库、电子商务等，是一个杰出的关系数据库平台，是信 息化C/S系统开发与管理的首选产品之一，越来越多的开发工具对它提供了编程支持与接 口，同时它为不同规模的用户提供如下帮助 (1) 通过构建、部署和管理，让企业的应用程序更加安全，伸缩性更强，更可靠。 (2) 可以降低开发和支持数据库应用程序的复杂性，实现IT生产力的最大化 (3) 在多个平台、应用程序和设备之间共享数据，更易于增强内、外部系统。 在不牺牲性能、可用性、可伸缩性和安全性的前提下有效控制成本。 (4)

## SQL Server 的发展过程

### 2.1.1

Microsoft SQL Server 起源于 Sybase 公司的 SQL Server。1988 年，Microsoft、Sybase 和 Ashton Tate 三家公司共同研制开发了 Sybase SQL Server，推出了第一个基于 OS/2 操作 系统的 SQL Server 版本。后来，Ashton Tate 公司由于某种原因退出了 SQL Server 的开发， Microsoft 则和 Sybase 签署协议，将 SQL Server 移植到 Microsoft 新开发的 Windows NT 操 作系统上，发布了用于 Windows NT 的 MS SQL Server 4，从此，双方的合作结束。Microsoft 开发并推广 Windows 环境中的 Microsoft SQL Server，简称 MS SQL Server; 而 Sybase 则 较专注于 SQL Server 在 UNIX 操作系统上的开发与应用。 MS SQL Server 6 是完全由 Microsoft 开发的第一个 SQL Server 版本，并于 1996 年升 级为 MS SQL Server 6.5。1998 年，Microsoft 发布了变化巨大的 MS SQL Server 7.0。2000 年，Microsoft 又很快发布了MS SQL Server 2000，采取了年号代替序号的策略，在功能和 性能上较以前版本有了巨大提高，并在系统中引入了对 XML 语言的支持。作为 MS SQL Server 产品发展的里程碑，MS SQL Server 6.5、MS SQL Server 7.0 和 MS SQL Server 2000 三个版本得到了广泛的应用。 2005 年 12 月，经过一波三折，Microsoft 艰难发布了Microsoft SQL Server 2005，它对 SQL Server 的许多地方进行了改写，对整个数据库系统的安全性和可用性进行了巨大的改 善，通过集成服务 （Integration Service）工具来加载数据，而其最大的改进是与.NET 构架 的紧密捆绑。 2008 年 3月，三年磨一剑的 Microsoft 发布了Microsoft SQL Server 2008，除了数据库 引擎和商业智能工具方面的提升外，加强了可以在引擎水平实施的透明数据加密功能及数 据库镜像功能，还重写了备份系统。并于 2010 年 5 月，发布 Microsoft SQL Server 2008 R2。 2012 年3月，Microsoft 正式发布了 Microsoft SQL Server 2012，较之前版本更具优势， 并增加了诸多激动人心的新功能，详见2.1.3节。

## SQL Server 2012 的体系结构

### 2.1.2

SQL Server 2012 是基于 C/S 模式的关系型数据库管理系统，严格按照 C/S 处理模式设 计，将事务处理合理地分配到客户机与服务器上，两者共同协调进行处理，能够充分发挥 客户机与服务器的各自优势和性能，减少网络流量，提高了整个系统的服务性能与效率。 例如，将输入、显示与校验数据这样需要用户频繁交互处理的任务分散在客户端的（多台） 机器上进行，而将读取共享数据、文件 IO 服务和数据查询处理等大流量的事务集中在数 据库服务器上完成，尽可能地发挥和利用服务器的高处理性能与客户机的交互灵活性，因 而提高了系统的性能与效率。 而在管理的具体实现上，SQL Server 2012 又灵活地分为单机管理架构、主从式管理架 构和分散式管理架构三种类型。 （1）单机管理架构。由同一台计算机包办数据库系统的所有工作，包括保存数据、处 理数据、管理及使用数据库系统等，即数据库服务器端和客户端都在同一台计算机上。 （2）主从式管理架构。在一台主机上安装 SQLServer 服务器，而在另外一些计算机上 安装相关的连接与管理程序 客户端，然后在客户端通过网络来操作及管理数据库服 务器。 25 （3）分散式管理架构。在主从式管理架构基础上增加多台数据库服务器，就构成了分 散式管理架构。在此架构中，可自由选择是将服务器端和客户端工具分开在不同主机上， 还是集中于同一台主机上。

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

SQLServer 是一个提供了联机事务处理、数据仓库、电子商务应用的数据库和数据分 析平台。体系结构是描述系统组成要素和要素之间关系的方式。SQL Server 2012 由两大部 分组成：数据库引擎和商业智能。 26 数据库引擎（SQL Server Database Engine,SSDE）是 SQL Server 2012系统的核心 服务，负责完成业务数据的存储、处理、查询和安全管理。在大多数情况下，使用数据库 系统实际上就是使用数据库引擎。例如，在选课信息管理系统中，学生选课数据的添加、 更新、删除、查询、安全控制等操作就由数据库引擎负责完成。实际上，数据库引擎本身 也是一个复杂的系统，包括了存储引擎、安全子系统、编程接口、复制、全文搜索、通知 服务等许多功能组件。 存储引擎，是数据库的“灵魂”组件，对基于表和列定义的数据存储进行管理，通 过数据存储管理组件控制着数据在磁盘上的存储方式和被应用程序访问的方式。比 如索引、分区、快照、锁定、事务、备份、恢复等。 安全子系统，是一个强大灵活的安全构架，确保数据和实例不被入侵。使用的手段 包括用户身份认证机制、引擎特性子集、多层次权限控制、多机制的数据加密方 式等。 编程接口，可通过T-SQL（Transact-Structured Query Language，事务结构化查询语 言，简称 T-SQL）进行编程，也可以使用满足CLR规范（Common Language Runtime, 公共语言运行规范，简称CLR）的编程语言对服务器功能进行扩展，如Visual Basic 和 Visual C#。引擎中直接集成的 XML 可访问 XML数据。 （Service Broker），在2005 版中引入，提供了异步通信机制，可以用于存 服务代理 储和传递消息。 SQL Server 代理（SQL Server Agent），是调度报警引擎。 快照复制，在不同数据库间对数据和数据库对象进行复制和分发，以保证数据库同 步和数据一致性。 高可用性组件，满足大量应用程序正常运行的需求，确保数据的可用性，包括故障 转移集群、数据库镜像、日志传送、复制技术等。 全文搜索，提供了基于关键字的企业级搜索功能。 通知服务，提供了基于通知的开发和部署平台。 （2）商业智能 （Business Intelligence，BI）是随着IT以及数据存储应用在商业应用中 的作用迅速扩大而出现的新成员，目的在于将分布在不同系统的大量数据整合为单一数据 集，构建强大的数据分析应用程序，并将信息合并到单独的分析系统。BI 包括3个组件: 分析服务、报表服务和集成服务。 ，分析服务（SQL Server Analysis Services,SSAS）提供联机分析处理(OnLine Analytical

## Processing，OLAP）和数据挖掘

(Data Mining， DM) 功能，可以支持用户建立数 据库。使用分析服务，可以设计、创建和管理包含来自于其他数据源数据的多维结 构，还可以完成数据挖掘模型的构造和应用，实现知识发现、表示和管理。例如， 选课信息管理系统中，可以使用分析服务完成对学生选课的数据挖掘分析，发现更 多有价值的信息和知识，从而更加合理地安排课程、提高课程管理水平。 报表服务（SQL Server Reporting Services，SSRS）为用户提供支持Web 的企业级报 表功能，可以方便地定义和发布满足自己需求的报表。例如，选课信息管理系统中， 可以使用报表服务方便地生成 Word、PDF、Excel 等各种格式的报表。 集成服务（SQL Server Integration Services，SSIS）是一个数据集成平台，可以完成 有关数据的提取、转换、加载等。它可以高效地处理各种各样的数据源，如Oracle、 Excel、XMIL 文档、文本文件等数据源中的数据。

# SQL Server 2012 的主要特性

### 2.1.3

作为新一版的 SQL Server，SQL Server 2012 仍然延续了以前版本的主要特点。

### 1．简单友好的操作方式

SQL Server 2012数据库管理系统继承了前一版的界面风格，包含一整套的管理和开发 工具。这些工具都具有非常友好的使用操作界面，既提供了强大的功能，同时又便于管理 和使用。

### 2．支持高性能的分布式数据库处理结构

SQL Server 2012 可以把工作负载划分到多个独立的 SQL Server 服务器上，使应用系统 中的数据可以存储在分散的多台服务器上，构成了分布式数据库体系，从而为实施电子商 务等大型系统提供了较好的可扩展性。

### 3．动态锁定的并发控制

SQL Server 通过隐含的动态锁定功能实现数据操作中的并发控制，有效地防止了在执 行查询和更新操作时出现冲突，既方便了开发者和用户，也提高了数据的共享可靠性。

### 4．丰富的编程接口并兼容以前版本

SQL Server 支持 T-SQL、DB Library for C/Visual Basic 和嵌入式 SQL 等多种开发工具， B 规范，允许使用 DBLIB、ODBC 和 OLEDB 的接口 而且还支持 DBLIB、ODBC、OLEDB 函数访问 SQLServer 数据库。基于以前版本建立的数据库与应用，可以非常可靠地运行在 SQL Server 2012 的数据库平台上。

### 5．单进程、多线程体系结构

SQL Server 2012 与其他多进程的 RDBMS 系统不同，采用单进程、多线程处理结构， 由执行内核统一分配和协调网络环境中多个用户对资源与数据的访问和存取，只需很小的 额外负担就可以同时处理多用户的并发访问，不但减少了内存的占用空间，而且有利于提 高和保持系统的运行速度、服务效率和稳定性。 在继承的基础上，SQL Server 2012又增加了一些新功能，具有自己的优势: （1）AlwaysOn。对镜像功能进行了提升，用户可对一组数据库做灾难恢复而非一个数 据库。 索引。为数据仓库查询设计的只读索引，扁平化压缩数据存储，减少 (2) Columnstore I/O和内存的使用。 （3）DBA 自定义服务器权限。支持对服务器的权限设置。 (4) Windows Server Core 支持。支持命令行界面的 WindowS，资源占用少、更安全。 27 Sequence Objects。支持列的自定义序列用对象实现 (5) （6）PowerVieW。强大的自主 BI工具，可让用户创建BI报告。 增强的审计功能。用户可自定义审计规则 (7)

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) (8） 增强的 PowerShell 支持。 （9）分布式回放（Distributed Replay）。可记录生产环境的工作状况，可在另一个环境 中重现。 28

## （10）SQL Azure 增强。

新功能的增加和原功能的改进使SQL Server 2012较SQL Server 2008更具以下优势： 方便易用。 (1) (2) 集成化的开发环境。 (3) 超快的性能。 (4) 安全性和高可用性。 (5) 企业安全性。 (6) 快速的数据发现 高效的数据压缩功能。 (7)

## SQL Server 2012 的版本

### 2.1.4

Microsoft SQL Server 2o12 版本分为主要版本、专业版本、延伸版本（也称扩展版本） 三类。其中，主要版本包括企业版、标准版、商业智能版，专业版本包括网络版，延伸版 本包括开发版、简易版等。用户可根据需求的不同选择版本。下面介绍各版本的简要特性。 (SQL Server 2012 Enterprise Edition)

### 1．企业版

SQLServer 2012 企业版是一个全面的数据管理和业务智能平台，为关键业务应用提供 了企业级的可扩展性、数据仓库、安全、高级分析和报表支持，作为生产数据库服务器使 用，支持 SQL Server 2012 中的所有可用功能，并可根据支持最大的 Web 站点和企业联机 事务处理（OLTP）及数据仓库系统所需的性能水平进行伸缩，为用户提供更加坚固的服务 器和执行大规模在线事务处理。它是当前所有版本中性能最好的，也是价格最贵的。作为 完整的数据库解决方案，该版本应该是大型企业首选的数据库产品。

### 2．标准版

(SQL Server 2012 Standard Edition) 该版本是一个完整的数据管理和业务智能平台，为部门级应用提供了最佳的易用性和 可管理特性。作为一般企业的数据库服务器使用，包括最基本的功能。虽然它的功能没有 企业版那样齐全，但它所具有的功能已经能够满足企业的一般要求，性价比较高。 (SQL Server 2012 Business Intelligence Edition)

### 3.．商业智能版

该版本提供了综合性平台，支持组织构建和安全部署、可扩展且易于管理的 BI解决 方案，提供基于浏览器的数据浏览与可见性等数据集成功能，增强集成管理。 (SQL Server 2012 Web Edition)

### 4．网络版

该版本是针对运行于 Windows 服务器中要求高可用、面向 Intermet Web 服务的环境而 设计。这一版本为实现低成本、大规模、高可用性的Web应用或客户托管解决方案提供了 必要的支持工具 (SQL Server 2012 Developer Edition)

### 5．开发版

供程序员用来开发将 SQL Server 2012 用作数据存储的应用程序。虽然开发版支持企业 版的所有功能，使开发人员能够编写和测试可使用这些功能的应用程序，但是只能将开发 版作为开发和测试系统使用，不能作为商业服务器使用。基于这一版本开发的应用和数据 库可以很容易地升级到企业版。 (SQL Server 2012 Express Edition)

### 6.．简易版

该版本也称学习版，与 MicrosoftVisual Studio集成，可以从微软网站免费下载使用， 拥有核心的数据库功能，其中包括了 SQL Server 20l2 中最新的数据类型，是 SQL Server 的一个微型版本。该版本是低端 ISV、低端服务器用户、创建 Web 应用程序的非专业开发 人员以及创建客户端应用程序的编程爱好者的理想选择。

# SQL Server 2012 的安装

### 2.2

# SQL Server 2012 安装前的准备工作

### 2.2.1

安装和使用 SQL Server 2012，计算机必须满足适当的硬件和软件要求。因此，在安装 SQL Server 2012 之前，应了解 SQL Server 2012 的特性，并检查所安装计算机的硬件和软 件的配置的情况，以保证其符合要求，从而避免在安装与使用过程中发生问题或故障。

### 1.SQL Server2012 安装的硬件条件

以 SQL Server 2012 企业版为例，其安装对计算机硬件的要求如表2-1 所示。如果想了 解其他版本的要求，请登录微软的官方 SQL资源网站，或者参考相应的安装文档。 表 2-1 SQLServer2012 企业版对硬件的要求 配置要求 硬件名称 类型: AMD Opteron, AMD Athlon 64, Intel Xeon with Intel EM64T support, 处理器 Intel Pentium IV with EM64T support (CPU) 建议：2.0GHz 或更高 最低主频：1.4GHz 最低：1GB 内存容量（RAM) 推荐：4GB 或更多 最多：全部计算机物理内存 系统驱动器中有至少 6.0GB 的可用磁盘空间，根据安装时所选组件的不 同，会有不同的要求。包括: 数据库引擎和数据文件、复制服务、全文检索服务、Data Quality Services: 811MB Analysis Services 和数据文件：345MB 硬盘空间（hard disk） Reporting Services 和报表管理：304MB Integration Services: 591MB Master Data Services: 243MB 客户端组件（不包括联机手册和集成服务工具）：1823MB SQL Server联机手册：375MB VGA（800X600 像素）或更高分辨率，图形工具要求 1024X768像素或 显示器（display） 更高的屏幕分辨率 鼠标（mouse） Microsoft 鼠标或其兼容鼠标 单机需要，也可以通过网络上的共享光盘驱动器CD/DVD-ROM进行安装 光盘驱动器 (CD-ROM) 在32位和64位平台上，支持8节点群集安装 群集硬件要求 29

### 2．SQL Server 2012 安装的软件条件

SQL Server 2012安装对计算机软件的要求包括以下几方面：

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) （1）操作系统。不同版本的 SQL Server 2012所支持的Windows 操作系统不尽相同 例如，64位企业版 SQL Server 2012 支持以下 Windows 版本： Windows Server 2012 R2 Datacenter 64 位 30 Windows Server 2012 R2 Standard 64 位. Windows Server 2012 R2 Essentials 64 位. Windows Server 2012 R2 Foundation 64 位 . Windows Server 2012 Datacenter 64 位。 Windows Server 2012 Standard 64 位。 Windows Server 2012 Essentials 64 位. Windows Server 2012 Foundation 64 位. Windows Server 2008 R2 SP1 Datacenter 64 位. Windows Server 2008 R2 SP1 Enterprise 64 位 . Windows Server 2008 R2 SP1 Standard 64 位. Windows Server 2008 R2 SP1 Web 64 位. Windows Server 2008 SP2 Datacenter 64 位. Windows Server 2008 SP2 Enterprise 64 位 。 Windows Server 2008 SP2 Standard 64 位. Windows Server 2008 SP2 Web 64 位. 其他版本的信息读者可以通过微软网站自行查询，此处不再赘述。 （2）其他软件环境的需求。对其他软件环境的要求如下： Framework。.NET Framework 4.0 及以上版本。 软件。Microsoft Windows Installer 4.5 或更高版本。 Windows PowerShell。对数据库引擎组件和 SQL Server Management Studio 而言, Windows PowerShell 2.0 是一个安装必备组件。 网络协议。操作系统已经内建了对 Shared memory（共享内存）、Named Pipes（命 名管道）、TCP/IP、VIA 协议的支持。 IE。需要 IE 7.0 或更高版本。 子（IS）。安装 SQL Server 2012 Reporting Services 需要 IIS 5.0 或更 Internet 信息服务 高版本。 ASP.NET 2.0。安装 SQL Server 2012 Reporting Services 需要 ASP.NET 2.0。

### 3．SQL Server 2012 安装前还应注意的其他问题

（1）对计算机系统做必要的计算机病毒、木马、黑客程序等安全方面的检查处理工作。 (2) 清除并关闭 Windows 事件查看器 (3) 配置安全的文件系统，建议使用NTFS。 (4) 使用具有管理员权限的用户账户登录相关的计算机系统 (5) 如果用户在安装过程中不清楚是否要选择某些功能或其具体含义，那么可以使用 默认值。

# 安装 SQL Server 2012

### 2.2.2

SQL Server 2012 的安装可以采用三种方式：安装向导安装、命令行安装和远程安装。 下面就以 SQL Server 2012 企业版全新实例的向导安装为例，介绍其本地安装过程并做简 要说明。其他版本的安装过程与之基本相同。安装环境以 MS Windows 7旗舰版为例。 （1）将 SQL Server 2012 安装光盘放入光驱，如果操作系统启用了自动运行功能，安装 程序将自动运行；或者直接运行安装文件目录下的 setup 文件来启动 SQL Server 2012的安 装。安装程序正常启动后打开图 2-l 所示的“SQL Server 安装中心”对话框，可以选择各 种计划。 SQLServer安装中心 计划 硬件和软件要求 查看硬件和软件要求。 安装 维护 安全文档 查看安全文档。 工具 资源 联机发行说明 查看有关该版本的最新信息 高级 选项 如何获取SQLServerDataTools SQLServerDataTools为数据库开发人员提供一个集成的环境，以便针对任何SQL Server平台执行所有数据库设计工作。 系统配置检查器 启动工具以检查阻止成功安装SQLServer的条件。 安装升级顾问 升级顾问会分析已安装的所有SQLServer2008R2、SQLServer2008或SQL Server2005组件，并确定在升级到SQLServer2012之前或之后要解决的问题。 联机安装帮助 启动联机安装文档。 如何开始使用SQLServer2012故障转移群集 阅读关于如何开始使用SQLServer2012故障转移群集的说明。 如何开始PowerPivotforSharePoint独立服务器安装 Microsoft

## SQLServer2012

请阅读有关如何用尽可能少>的步骤在新SharePoint2010服务器上安装PowerPivot forharaDoint的说B

图 2-1 “SQL Server 安装中心”对话框 安装中心为用户提供了丰富的信息和合理的安装计划，包括了在安装 SQL Server 2012 前应了解的基本信息，为确定安装方案做好准备。其中，SQL Server升级顾问可以根据已 有的系统提供 SQL Server 升级方案。还包括了 SQL Server 的各种相关信息以及信息的获取 途径，有助于用户更好地掌握 SQL Server 系统。 ，，（） 现有安装添加功能”选项，如图 2-2 所示。等待安装程序完成一些前期准备工作后进入下 一步。 (3） 当前操作处理完成后，将打开“SQL Server 2012 安装程序”对话框，出现“安装 程序支持规则”选项，根据当前系统的具体情况，一些检查已经通过了，如图 2-3所示。 31 单击“确定”按钮，可以进入下一步。

SQL Server 2012 综述

## 数据库原理与技术

(SQL Server 2012) SQLServer安装中心 全新SQLServer独立安装或向现有安装添加功能 计划 启动向导，在非群集环境中安装SQLServer2012或向现有SQLServer2012实例中 安装 添加功能。 维护 32 新的SQLServer故障转移群集安装 工具 启动向导，安装单节点的SQLServer2012故障转移群集。 资源 向SQLServer故障转移群集添加节点 高级 启动向导，向现有SQLServer2012故障转移群集中添加节点。 选项 启动向导，将SQLServer2005、SQLServer2008或SQLServer2008R2升级到 SQLServer2012.

Microsoft

## SQL Server2012

图 2-2 选择“全新SQL Server 独立安装或向现有安装添加功能”选项

SQLServer2012安装程序 安装程序支持规则 安装程序支持规则可确定在您安装SQL Server安装程序支持文件时可能发生的问题。必须更正所有失败，安装程序才能 继续。 操作完成。已通过：8。失败0。警告0。已跳过0。 安装程序支持规则

重新运行(R) 隐藏详细信息(S)< 查看详细报表（V 状态 规则 已通过 安装程序管理员 设置帐户权限 已通过 已通过 重新启动计算机 WindowsManagementInstrumentation(WMI)服务 已通过 已通过 针对SQLServer注册表项的一致性验证 已通过 SQLServer安装介质上文件的长路径名称 已通过 SQLServer安装程序产品不兼容 用于Windows2008R2和Windows7的.NET2.0和.NET... 已通过

取消 确定

图 2-3 “安装程序支持规则”选项 （4）在输入产品密钥的提示页面，在“输入产品密钥”框中输入正确的密钥，如图2-4 所示，单击“下一步”按钮继续安装；或者在“指定可用版本”中选择Evaluation 版（测 试版）或Express 版（简易版）等免费版本进行安装。此例是通过产品密钥进行企业版的 安装。 SQLServer2012安装程序 产品密钥 指定要安装的SQLServer2012版本。

请通过输入Microsoft真品证书或产品包装上的由25个字符组成的密钥来验证比SQLServer2012实 产品密钥 例。您也可以指定SQLServer的免费版本，例如Evaluation或Express，如SQLServer联机丛书中所 许可条款 本，请运行版本升级向导。 产品更新 安装安装程序文件 ①指定可用版本(S): Evaluation 输入产品密钥（E)： 748RBX4T6BMRM7VRTVFF-CHC8H

下一步(N) × 取消 ×上一步(B)

图 2-4 验证产品密钥 （5）在“许可条款”选项页中选择“我接受许可条款”选项，如图2-5所示。单击“下 一步”按钮继续安装， SQLServer2012安装程序 许可条款 若要安装SQLServer2012，必须接受Microsoft软件许可条款。

产品密钥 MICROSOFT软件许可条款 许可条款 MICROSOFTSQLSERVER2012ENTERPRISESERVER/CALEDITION 产品更新 安装安装程序文件 这些许可条款是MicrosoftCorporation（或您所在地的MicrosoftCorporation关联公司）与您之 间达成的协议。请阅读条款内容。这些条款适用于上述软件，包括您用来接收该软件的介质（如 有）。这些条款也适用于Microsoft为该软件提供的任何 更新 补充程序 基于Internet的服务和

复制(C) 打印(P) 我接受许可条款(A)。 将功能使用情况数据发送到Microsoft。功能使用情况数据包括有关您的硬件配置以及您对SQL Server及其组件的使用情况的信息（D。 有关详细信息，请参阅MicrosoftSQLServer2012隐私声明。 下一步(N) > 取消 ≤上一步(B)

图 2-5 接受安装许可条款 （6）为了SQL Server 的安全性和性能，需要始终安装最新的更新，如图 2-6 所示。

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) SQLServer2012安装程序 产品更新 始终安装最新的更新以增强SQLServer安全性和性能。

产品密钥 34 包括SQLServer产品更新(D) 许可条款 详细信息 名称 大小(MB) 产品更新 145 KB 2793634 SQL Server2012 SP1 GDR Pr... 安装安装程序文件 KB 2793634 26 SQL Server 2012 SP1 GDR Set...

在线找到2个更新(171MB)。 在单击下一步"时将安装安装程序更新(26MB)。

在线阅读我们的隐私声明 了解有关SQLServer产品更新的详细信息

下一步(N) > 取消 上一步(B)

图 2-6 进行产品更新 （7）在图2-6中单击“下一步”按钮，进入“安装安装程序文件”选项页，如图2-7 所示。单击“安装”按钮，将安装前一步检查到的产品更新和安装SQL Server 程序所需的 组件。 SQLServer2012安装程序 安装安装程序文件 将立即安装SQLServer安装程序。如果找到SQLServer安装程序的更新并指定要包含在内，则也将安装更新。

产品密钥 许可条款 正在下载安装文件：已下载16MB，共26MB（60%） 产品更新 任务 状态 安装安装程序文件 已完成 扫描产品更新 正在进行 下载安装程序文件 未启动 提取安装程序文件 未启动 安装安装程序文件

安装(D 取消 上一步(B)

图 2-7 安装程序支持文件 （8）上述安装完成后，程序将自动进行第二次支持规则的检测，如图 2-8所示。检测 全部通过后才能进行下一步的角色设置。 SQLServer2012安装程序 安装程序支持规则 安装程序支持规则可确定在您安装SQL Server安装程序支持文件时可能发生的问题。必须更正所有失败，安装程序才能 继续。 安装程序支持规则 操作完成。已通过：6。失败0。警告1。已跳过0。 设置角色 功能选择 安装规则 隐藏详细信息（S) 重新运行(R) 磁盘空间要求 查看详细报表(V) 错误报告 规则 状态 安装配置规则 已通过 合成活动模板库(ATL) 准备安装 早期版本的SQLServer2008BusinessIntelligenceDevelo.. 安装进度 已通过 已通过 完成 没有与SQLServer"Denali"CTPO一同安装的SxS 已通过 针对SQLServer注册表项的一致性验证 计算机域控制器 已通过 Microsot.NET应用程序安全性 上通过 警告 Windows防火墙

下一步(N) > 取消 帮助 ≤上一步(B)

图 2-8 安装程序支持规则 （9）在“设置角色”选项页中选择“SQL Server功能安装”，如图2-9所示。单击“下 一步”按钮继续安装。 SQLServer2012安装程序 设置角色 单击“SQLServer动能安装”选项以逐个选择要安装的功能组件，或单击某个功能角色以安装特定配置。

安装程序支持规则 SQLServer功能安装(S) 设置角色 安装SQLServer数据库引擎服务.AnalysisServices.ReportingServices.IntegrationServices 和其他功能。 功能选择 安装规则 SQL Server PowerPivot forSharePoint(P) 磁盘空间要求 在新的或现有的SharePoint服务器上安装PowerPivotforSharePoint以支持场中的PowerPivot数 据访问。或者，添加SQLServer关系数据库引擎以便用作新场的数据库服务器。 错误报告 将SQLSerVer数据库关系引擎服务添加到此安装(R)。 安装配置规则 准备安装 具有默认值的所有功能(D) 安装进度 使用服务帐户的默认值安装所有功能。 完成

帮助 取消 ≤上一(B) 下一步(N) >

图 2-9 设置角色 （10）进入“功能选择”选项页，进行要安装的功能选择。为了使用的方便，在空间 35 足够的情况下，可以使用“全选”安装全部功能组件，如图2-10所示。单击“下一步”按 钮继续安装。

SQL Server 2012 综述 (SQL Server 2012)

## 数据库原理与技术

SQLServer2012安装程序 功能选择 选择要安装的Enterprise功能。 36 功能(E): 安装程序支持规则 功能说明: 设置角色 实例功能 SQLServer实例的每个实例功能的配置和操 功能选择 作都与其他SQLServer实例分开。 数据库引擎服务 SQLServer实例可以在同一台计算机上并行 SQLServer复制 安装规则 操作。 全文和语义提取搜素 实例配置 Data Quality Services 磁盘空间要求 Analysis Services 服务器配置 Reporting Services-本机 所选功能的必备组件(P)： 数据库引擎配置 共享功能 已经安装： Reporting Services - SharePoint Analysis Services配置

### I.. Windows PowerShell 2.0

用于SharePoint产品的ReportingServices ReportingServices配置

### I.. Microsoft .NET Framework 3.5

数据质量客户端 分布式重播控制器 要从介质安装： SQLServer DataTools ..Microsoft.NETFramework4.0(可能需 分布式重播客户端 客户端工具连接 错误报告 安装配置规则 全选(A) 全部不选(U 准备安装 共享功能目录(S): C:(Program Files\Microsoft SQL Server) 安装进度 完成 共享功能目录(x86)(): C:(Program Files (x86)\Microsoft SQL Serverl 下一步(N) > 取消 帮助 ≥上一步(B)

图 2-10 功能选择 （11） 完成功能选择后，进入“安装规则”选项页，系统自动进行安装规则信息检查， 如图2-11所示。检查均通过后单击“下一步”按钮继续安装 窗SQLServer2012安装程序 安装规则 安装程序正在运行规则以确定是否要阻止安装过程。有关详细信息，请单击“帮助”。

安装程序支持规则 操作完成。已通过：4。失败0。警告0。已跳过0 设置角色 功能选择 重新运行(R) 安装规则 隐藏详细信息(S) 实例配置 查看详细报表（V) 磁盘空间要求 规则 状态 服务器配置 已通过 数据库引擎配置 需要更新的以前的VisualStudio2010实例。 已通过 Analysis Services配置 SQLServerAnalysisServices服务器模式和版本检查 已通过 产品更新语言兼容性 Reporting Services配置 已通过 需要Microsoft.NETFramework3.5ServicePack1 分布式重播控制器 分布式重播客户端 错误报告 安装配置规则 准备安装 安装进度 完成

下一步(N) > 取消 帮助 ≤上一步(B)

图 2-11 安装规则 （12）在“实例配置”选项页选择“默认实例”，并设置实例的根目录，如图2-12所示。

## 单击“下一步”按钮继续安装。

SQLServer2012安装程序 实例配置 指定SQL Server实例的名称和实例ID。实例ID将成为安装路径的一部分。 安装程序支持规则 默认实例(D) 设置角色 命名实例(A): MSSQLSERVER 功能选择 安装规则 实例配置 MSSQLSERVER 实例ID(): 磁盘空间要求 实例根目录(R): C:\Program Files\Microsoft SQL Serverl 服务器配置 数据库引擎配置 AnalysisServices配置 SQLServer目录： C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER Reporting Services配置 C:\Program Files\Microsoft SQL Server\MSAS11.MSSQLSERVER AnalysisServices目录： 分布式重播控制器 ReportingServices目录:C:\ProgramFiles\Microsoft SQLServer/MSRS11.MSSQLSERVER 分布式重播客户端 错送报告 已安装的实例(L): 安装配置规则 实例名称 功能 版本类别 版本 实例ID 准备安装 安装进度

取消 帮助 下一步(N) <上一步(B)

图 2-12 实例配置 有关 SQL Server 的“实例”特性说明如下: SQL Server 允许在一台计算机上执行多次安装，每一次安装都是一个实例。一个实 例就是一组配置文件和运行在计算机内存中的一组程序。从简单的角度来说，用户 可以把一个实例理解为一个 SQL Server 服务器。而所谓“多实例环境”，则可以认 为就是在一台计算机上安装的多个 SQL Server 服务器。 SQL Server 2012默认实例。该实例由运行它的计算机的网络名称标识。一台计算机 上只能有一个默认实例。 SQL Server 2012 的命名实例。该实例通过计算机的网络名称加上实例名称以“计算 机名称I实例名称”的格式进行标识。应用程序必须使用 SQL Server 2012 客户端组 件连接到命名实例。计算机可以同时运行多个 SQL Server 2012 命名实例。 新实例名称必须以字母、“和”符号（＆）或下画线（）开头，可以包含数字、字 母或其他字符。SQL Server 系统名称和保留名称不能用作实例名称。例如，default 一词不能用作实例名称，因为它是安装程序使用的保留名称 多实例。当一台计算机安装有多个 SQL Server 2012 实例时，就会出现多实例。每 个实例的操作都与同一台计算机上的其他任何实例分开，而应用程序可以连接任何 实例。在单台计算机上可以安装的实例数是有限的，取决于可用资源，不同的版本 有不同的限制。若默认服务器实例已经安装，以后再安装只能安装命名实例服务器。 在未安装过 SQL Server 的计算机上安装 SQL Server 2012 时，安装程序默认安装默 认实例。但是，通过选择“命名实例”并给定命名实例名，也可以选择将 SQL Server 2012 安装为命名实例， 37 可以在下列任意时间安装 SQL Server 2012 命名实例。安装 SQL Server 2012 默认实 例之前、安装 SQL Server 2012 默认实例之后或者取代安装 SQL Server 2012 默认实 例。每个命名实例都由非重复的一组服务组成，并且对于排序规则和其他选项可以

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) 有完全不同的设置。目录结构、注册表结构和服务名称都反映了所指定的具体实例 名称。 （13）在“磁盘空间要求”选项页中，显示存储空间资源信息及磁盘使用情况、需求， 38 如图2-13所示。单击“下一步”按钮继续安装。 SQLServer2012安装程序 磁盘空间要求 查您选择的SQLServer功能所需的磁盘空据要，

磁盘使用情况摘要： 安装程序支持规则 设置角色 日驱动器C:需要8946MB，有27759MB可用 功能选择 系统驱动器（C:V):需要5010MB 共享安装目录（C>ProgramFiles/MicrosoftSQLServerN:需要1642MB 安装规则 实例目录(C:)ProgramFiles)MicrosoftSQLServerV：需要2294MB 实例配置 磁盘空问要求 服务器配置 数据库引擎配置 Analysis Services配置 Reporting Services 配置 分布式重福控制器 分布式重播容户端 错误报告 安装配置规则 准备安装 安装进度 完成

取消 帮助 下一步(N) > 上一步(B)

图 2-13 磁盘空间要求 （14）进入“服务器配置”选项页，设置使用 SQLServer各种服务的用户，可以按默 认情况安装，也可以将账户名称统一选择为NTAUTHORITY\ISYSTEM（本地主机的系统 用户），如图2-14所示（本例按默认情况安装）。单击“下一步”按钮继续安装。 窗 SQL Server 2012 安装程序 服务器配置 指定服务帐户和排字规则配置

安装程序支持规则 服务帐户 排序规则 设置角色 Microsoft建议您对每个SQLServer服务使用一个单独的帐户(M)。 功能选择 服务 密码 帐户名 启动类型 安装规则 手动 SQL Server 代理 NT Service\SQLSERVE... 实例配置 自动 SQLServer数据库引擎 NT Service\MSSQLSE... 磁盘空间要求 自动 NT Service\MSSQLSer... SQL Server Analysis Services 服务器配置 自动 NT Service\ReportSer... SQL Server Reporting Services 数据库引擎配置 自动 NT Service\MsDts Serv... SQL Server Integration Service... Analysis Services 配置 手动 SQL Server Distributed Replay ... NT Service\SQL Serve... ReportingServices配置 手动 SQL Server Distrilbuted Replay ... NT Service\SQL Serve... 分布式重播控制器 手动 SQL Full-text Filter Daemon Lau... NT Service\MSSQLFD... 分布式重播客户端 SQL Server Browser NT AUTHORITY,LOCA... 错误报告 安装配置规则 准备安装 安装进度 完成 取消 帮助 ≤上一步(B) 下一步(N)>

图 2-14 服务器配置 （15）进入“数据库引擎配置”选项页，设置SQLServer 2012的身份验证模式及管理 员信息，如图2-15所示，本例中采用默认的“Windows 身份验证模式”，并添加当前用户 为管理员，单击“下一步”按钮继续。若选择采用“混合模式”，则需要指定

# SQL Server

系统管理员（sa）的登录密码。 SQL Server 2012 安装程序 数据库引擎配置 指定数据库引擎身份验证安全模式、管理员和数据目录。

安装程序支持规则 服务器配置 FILESTREAM 数据目录 设置角色 为数据率引擎指定身份验证模式和告理员。 功能选择 安装规则 身份验证模式 实例配置 Windows身份验证模式(W) 磁盘空间要求 混合模式(SQLServer身份验证和Windows身份验证)(M) 服务器配置 为SQLServer系统管理员(sa)帐户指定密码。 数据库引挚配置 Analysis Services 配置 输入密码(E): Reporting Services配置 确认密码(O): 分布式重控制器 指定SQLServer管理员 分布式重播客户端 错误报告 SKY-20170310IRLVAdministrator (Administrator) SQLServer管理员对数 据库引擎具有无限制的访 安装配置规则 问权限。 准备安装 安装进度 添加A... 删除(R) 添加当前用户[0] 完成 取消 帮助 ≤上一步(B) 下一步(N)

图 2-15 数据库引擎配置 SQL Server 2012 系统的账户设置分为内置系统账户和域用户账户两类。一般建议使用 内置系统账户中的本地系统账户，但是本地系统账户和网络服务账户具有较大的权限，在 使用时要考虑好系统的安全性。 用户也可以不为 sa 账户指定密码，但这种方法不安全，故不提倡采用。在完成 SQL Server安装之后，根据需要，用户在 SQLServer服务器中可重新设置用户身份验证模式。 关于登录账户和身份验证问题，在2.3节会做进一步的介绍。 （16）在“Analysis Services 配置”选项页中，添加当前用户，如图2-16所示。单击“下 一步”按钮继续安装。 SQL Server 2012安装程序 AnalysisServices配置 指定Analysis Services服务器模式。管理员和数据目录, 安装程序支持规则 数据目录 服务器配置 设置角色 服务器模式： 功能选择 多维和数漏挖掘模式(M) 安装规则 ①表格模式(D 实例配置 指定哪些用户具有对AnalysisServices的告理权限。 磁盘空间要求 SKY-20170310IRLVAdministrator (Administrator) Analysis Services管理员 服务器配置 对Analysis Services具 数据库引擎配置 有不受限制的访问权限。 Analysis Services 配置 Reporting Services 配置 分布式重福控制器 分布式重播容户端 错误报告 安装配置规则 准备安装 安装进度 添力加(A). 删除(R) 添加当前用户(C) 完成 39 帮助 取消 ≤上一步(B) 下一步(N)>

Analysis Services 配置 图 2-16

SQL Server 2012 综述 (SQL Server 2012)

## 数据库原理与技术

（17）在“Reporting Services 配置”选项页中，按照默认的设置，选中“安装和配置”, 如图2-17所示。单击“下一步” 按钮继续安装。 SQL Server2012安装程序 40 ReportingServices配置 指定ReportingServices配置模式。 ReportingServices本机模式 安装程序支持规则 设置角色 安装和配置（C)。 功能选择 在本机模式中安装和配置报表服务器。报表服务器将在安装完成后正常运行。 安装规则 ①仅安装(Q)。 实例配置 安装报表服务器文件。安装完成后，使用Reporting Services配置管理器配置报表服务器用于 磁盘空间要求 本机模式 服务器配置 ReportingServicesSharePoint集成模式 数据库引擎配置 仅安装(S)。 Analysis Services配置 安装报表服务器文件。安装完成后，使用SharePoint管理中心完成配置。确认SQLServer Reporting Services配置 ReportingServices服务已启动并且创建至少一个SQLServerReportingServices服务应用 程序。有关详细信息，请单击“帮助”： 分布式重播控制器 分布式里摧客户端 错误报告 安装配置规则 准备安装 安装进度 完成

帮助 取消 ≤ 上一步(B) 下一步(N) >

图 2-17 Reporting Services 配置 （18）在“分布式重播控制器”选项页中，将当前用户设为授予针对分布式重播控制 器服务的管理权限的用户，可以不受限制地访问分布式重播控制器服务，如图2-18所示。 单击“下一步”按钮继续安装， SQLServer2012安装程序 分布式重播控制器 指定分布式重播控制器服务的访问权限。

安装程序支持规则 指定哪用户具有对分布式重播控制器服务的权限。 设置角色 SKY-20170310IRLVAdministrator (Administrator) 被授予权限的用户将可以不 功能选择 受限制地访问分式重播控 制器服务。 安装规则 实例配置 磁盘空间要求 服务器配置 数据库引擎配置 Analysis Services配置 Reporting Services 配置 分布式重播控制器 分布式重播客户端 错误报告 安装配置规则 准备安装 安装进度 完成 添加A.. 添加当前用户(C) 删除(R) 取消 帮助 ≤上一步(B) 下一步(N) >

图 2-18 分布式重播控制器 （19）在“分布式重播客户端”选项页中，在“控制器名称”文本框中输入一个合法 标识符作为控制器名称，也可不指定，并设置工作目录和结果目录，一般采用默认设置， 如图2-19所示。单击“下一步”按钮继续安装。 SQLServer2012安装程序 分布式重播客户端 为分布式重播客户端指定相应的控制器和数据月录，

安装程序支持规则 指定控制器计算机的名称和目录位置。 产品密钥 控制器名称(C): 许可条款 工作目录(W: C:\Program Files (x86)\Microsoft SQL Server/DReplayClientWorkingCir) 设置角色 功能选择 结果目录(R): C:Program Files (x86)Microsoft SQL Server)DReplayClient(ResultDir) 安装规则 实例配置 磁盘空间要求 服务器配置 数据库引擎配置 AnalysisServices配置 Reporting Services配置 分布式重播控制器 分布式重播客户端 错误报告 安装配置规则 准备安装

下一步(N) > 帮助 上一步(B) 取消

图 2-19 分布式重播客户端 （20）进入“错误报告”选项页，根据自已的需要进行选择，单击“下一步”按钮继 续安装，如图2-20所示。 SQLServer2012安装程序 错误报告 帮助Microsoft改进SQLServer功能和服务。

指定您希望自动发送到Microsoft以改进SQLServer未来版本的信息。这些设置是可选的。Microsoft 安装程序支持规则 会将该信息视为机密信息。Microsoft可能会通过MicrosoftUpdate提供更新以修改功能使用情况数 设置角色 据。根据您的“自动更新”设置，这些更新可能会自动下载并安装到您的计算机上。 功能选择 安装规则 实例配置 有关详细信息，请参阅MicrosoftSQLServer2012隐私声明， 磁盘空间要求 阅读有关MicrosoftUpdate和自动更新的更多信息。 服务器配置 数据库引擎配置 将Windows和SQLServer错误报告发送到Microsoft或您公司的报表服务器。该设置仅适用于以 Analysis Services配置 无用户交互方式运行的服务（W)。 ReportingServices配置 分布式重播控制器 分布式重播客户端 错误报告 安装配置规则 准备安装 安装进度 完成

下一步(N) > 取消 帮助 《上一步(B)

41 错误报告 图 2-20 （21）在“安装配置规则”选项页中，再次对系统进行检测，如果全部通过，单击“下

SQL Server 2012 综述 (SQL Server 2012)

## 数据库原理与技术

一步”按钮继续安装，如图2-21所示 SQLServer2012安装程序 安装配置规则 42 安装程序正在运行规则以确定是否要阻止安装过程。有关详细信息，请单击“帮助”。 操作完成。已通过：7。失败0。警告0。已跳过0。 安装程序支持规则 设置角色 功能选择 安装规则 隐藏详细信息（S) 重新运行(R) 实例配置 查看详细报表(V) 磁盘空间要求 规则 状态 服务器配置 已通过 数据库引擎配置 FAT32文件系统 Analysis Services 配置 已通过 现有群集实例或准备好群集的实例 已通过 ReportingServices配置 跨语言安装 已通过 分布式重播控制器 相同体系结构安装 分布式重播客户端 已通过 ReportingServices目录数据库文件存在 错误报告 已通过 ReportingServices目录临时数据库文件存在 安装配置规则 已通过 SQLServerAnalysisServices服务器模式和版本检查 准备安装 安装进度 完成

下一步(N) > 取消 帮助 ≤上一步(B)

图 2-21 安装配置规则 （22）在“准备安装”选项页中，可以看到要安装的功能选项，单击“安装”按钮继 续安装，如图2-22 所示。 SQLServer2012安装程序 准备安装 验证要安装的SQLServer2012功能。

安装程序支持规则 已准备好安装SQLServer2012： 设置角色 日-摘要 功能选择 .版本类别：Enterprise 操作：Install(产品更新) 安装规则 白·必备组件 实例配置 白·已经安装： 磁盘空间要求 -. Windows PowerShell 2.0 服务器配置 ...Microsoft.NETFramework3.5 数据库引擎配置 白·要从介质安装： .Microsoft.NETFramework4.0(可能需要重新引得) AnalysisServices配置 .. Microsoft Visual Studio  2010 Shell Reporting Services配置 ... Microsoft Visual Studio Tools for Applications 3.0 分布式重播控制器 白·常规配置 分布式重播客户端 白·功能 错误报告 数据库引擎服务 SQLServer复制 安装配置规则 准备安装 安装进度 配置文件路径： 完成 C:/Program Files\Microsoft SQLServer/1101Setup Bootstrap/Log\/20170312_150501\Configurationl 安装(I) 取消 帮助 上一步(B)

图 2-22 准备安装的信息 （23）在“安装进度”选项页中，可以看到正在安装 SQL Server 2012。耐心等待 SQL Server 2012 安装过程完成，若没有错误，则单击“下一步”按钮继续安装，如图2-23所示。 SQLServer2012安装程序 安装进度

安装程序支持规则 设置角色 功能选择 Install_DotNetCore_Cpu64_Action 安装规则 实例配置 磁盘空间要求 服务器配置 数据库引擎配置 AnalysisServices配置 Reporting Services配置 分布式重播控制器 分布式重播客户端 错误报告 安装配置规则 准备安装 安装进度 完成

取消 帮助 下一步(N)>

图 2-23 安装进度 （24）在“完成”选项页中，可以看到“SQL Server 2012 安装已成功完成”的提示， 单击“关闭”按钮结束安装，如图2-24所示。 SQL Server2012安装程序 完成 SQLServer2012安装已成功完成带产品更新。

安装程序支持规则 关于安装程序操作或可能的随后步骤的信息(D)： 产品密钥 状态 功能 许可条款 管理工具-完整 成功 设置角色 客户端工具连按 成功 功能选择 成功 客户端工具SDK 安装规则 成功 客户端工具向后兼容性 管理工目其本 Th 实例配置 磁盘空间要求 服务器配置 详细信息(D): 数据库引擎配置 查看有关SQLServer的产品文档 Analysis Services配置 只安装了您用于查看和管理SQLServer文档的组件。在默认情况下，“帮助查看器"组件使用联机 ReportingServices配置 库。在安装SQLServer之后，您可以使用帮助库管理器"组件将文档下载到您本地计算机。有关 分布式重播控制器 详细信息，请参阅使用MicrosoftSQLServer联机A书 <http://g0.microsoft.com/fwlink/?LinkID=2246B3>o 分布式重播客户端 错误报告 已将摘要日志文件保存到以下位置： 安装配置规则 C:\ProgramFiles/Microsoft SQLServer/1101SetupBootstrap\Log/20170312182911 准备安装 SummarySKY-20170310IRL20170312182911.txt 关闭 帮助

图 2-24 安装完成 到此，整个 SQL Server 2012 的安装顺利完成，根据提示重新启动计算机即可。

## 升级到 SQL Server 2012

### 2.2.3

在网络应用系统的维护中，会遇到需要保留原有系统中的数据并升级到 J SQL Server

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) 2012 的情形。SQL Server 2012 支持从 SQL Server 2005、SQL Server 2008 升级。升级到 SQL Server 2012 需要有很好的准备，否则会有丢失数据或新旧版本不能平滑过渡的风险。 44 擎）、升级指定的数据库和数据库对象。针对不同的升级内容可以采取不同的升级方式。若 对整个系统或某个组件进行升级，采用 Microsoft 公司提供的 SQL Server 2ol2 升级顾问是 最适当的升级方式。若仅升级指定的数据库和数据库对象，则可以采取迁移、备份和恢复

## 等方式。

### 1．SQL Server 2012 升级顾问

启动 SQL Server 2012 安装，打开如图2-1所示的 SQL Server 2012 安装中心对话框， 选择“计划”选项中的“安装升级顾问”选项来安装升级顾问。安装完毕后，运行升级顾 问可以启动以下工具：升级顾问分析向导、升级顾问报表查看器、升级顾问帮助， 使用升级顾问可以评估当前的 SQL Server 安装、组件及相关文件，从而标识出会在升 级或迁移到 SQL Server 2012 的过程中和过程后出现的问题。在升级顾问报表中，阻碍 SQL Server 2012升级的问题将被标识为升级障碍。如果障碍未得到解决，将自动退出安装

### 2．SQLServer 2012 升级顾问分析向导

升级顾问分析向导会引导用户逐步完成升级的工作，其运行分为以下5个阶段： (1) 确定要分析的服务器和组件。 (2) 收集其他参数。 (3) 收集身份验证信息。 (4) 分析所选组件。 (5) 生成升级问题报表 升级顾问的主要作用是帮助用户定位升级 SQL Server 2012 时无法完成或实现的任务 和功能。但是该功能不能帮助用户自动地完成一切升级工作。在找到无法实现的功能后 用户还需要自己对程序做进一步的升级。 升级到 SQL Server 2012 的方法有两种：并行法（移植法）和取代升级法。 在移植法中，SQL Server 2012 可作为一个独立实例与 SQL Server 2008/2005 安装在一 起。对于这种情况，必须将用户的数据库从老式数据库实例中分离出来并添加到新的实例 中去。SQL Server 2008/2005 升级到 SQL Server 2012 的方法为: （1） 数据库引擎一一并行安装，然后进行数据库备份/恢复，分解/合并。 移植向导对象，需要客户升级。 (2） Analysis Services-

## (3） Integration Services

移植向导转换50%～70%的任务，因此还需要一些手动移植。

## (4） Reporting Services

并行安装，以新实例发布报告。 (5） Notification Services 在安装过程中更新通知服务实例。 使用取代法，SQL Server 2012 可以安装在 SQL Server 2008/2005 的原有安装路径下， 但此时，所有原来的数据库实例和账号都被移除。

## SQL Server 2012 安装成功的验证

### 2.2.4

SQL Server 2012 安装过程中没有出现错误提示，一般可以认为 SQL Server 2012 是安 装成功的，但也可以通过一些简单的方式来初步验证 SQL Server 2012是否安装成功。

### 1．验证“开始”菜单中的程序组

MicrosoftSQLServer2012 安装完成后用户可以通过查看“开始”菜单中的SQL coSQLServerDataTools Server 2012 程序组应用程序来验证 SQL Server 2012 是否安 SQLServerManagementStudio 导入和导出数据(32位) 装成功。 导入和导出数据(64位) 下载MicrosoftSQLServerComp SQL Server 2012 安装成功后，会在 Windows 的“开始” Analysis Services Configuration Tools 菜单的“程序”级联菜单中添加 SQL Server 2012 应用程序 Data Quality Services Integration Services 组，如图2-25所示，供用户访问其应用程序。 Master Data Services 配置工具

### 2．启动 SQL Server 2012 程序

厨ReportingServices配置管理器 国SQLServer错误和使用情况报 可以通过检查 SQL Server 2012 服务是否能成功启动， 高SQLServer配置管理器 进一步验证 SQL Server 2012 安装是否成功。 文档和社区 SQLServer文档 可以用以下 4 种方法来启动 SQL Server 2012 程序: 管理帮助设置 社区项目和示例 (1） 安装过程中设置 SQL Server 2012 程序自动启动。 资源中心 性能工具 （2）用SQL Server 配置管理器（SQL Server Configuration SQL Server Profiler 数据库引擎优化顾问 Manager）启动。选择“开始”→“所有程序”→Microsoft SQL “器O，“首， 返回 令，打开如图 2-26所示中的 Sql Server Configuration Manager 搜素程序和文件 窗口，单击左窗格中的“SQL Server 服务”选项，则在右窗 格中会显示各项服务的启动情况。右击任何一项服务，在弹 图 2-25 SQL Server 2012 程序组 丛“，“，“，中 项服务进行操作。 SqlServerConfigurationManager 文件(F) 查看（M) 帮助(H) 操作(A)

SQLServer配置管理器（本地） 状态 进程ID 名称 启动模式 登录身份为 目SQLServer服务 SQLServerIntegrationServices11.0 正在运行 自动 NT Service\MsDts... 1964 早SQLServer网络配置(32位) 手动 sQLFull-textFilterDaemonLauncher... NT Service\MSSQ... 2996 正在运行 享SQLNativeClient11.0配置(32位） SQLServer(MSSQLSERVER) 1384 NTServicelMSSQ.. 早.SQLServer网络配置 启动(S) SQLServerAnalysisServices(MSSQ.. NTService\MSSQ... 1420 学SQLNativeClient11.0配置 停止(O) SQLServerReportingServices (MSS. NT Service\Repor... 2056 暂停(P) SQLServerBrowser ..NTAUTHORITYL... 继续(E) SQLServer代理（(MSSQLSERVER) NTServicelSQLSE... 重新启动(T) 属性(R) 帮助(H) 暂停所选服务。

图 2-26 用 SQLServer配置管理器启动服务 （SQL Server Management Studio）启动。用户可以通过 （3）用 SQL Server 集成管理器 SQL Server Management Studio 来启动、暂停、继续和终止 SQL Server 2012 服务。右击 SQL Server Management Studio 窗口左窗格中的服务器，在弹出的快捷菜单中选择“启动”命令， 即可启动 SQL Server 2012程序，如图2-27所示。 (4） 通过操作系统的“控制面板”中的“服务”窗口启动。用户可以通过“服务”窗 45 口来直接启动、暂停、继续和终止 SQL Server 2012 服务。通过“控制面板”→“系统和安 全”→“管理工具”找到“服务”选项图标，打开“服务”窗口，右击相应的SQLServer 2012 服务，在弹出的快捷菜单中选择“启动”命令即可，如图2-28所示。

SQL Server 2012 综述 (SOL Server 2012)

## 数据库原理与技术

MicrosoftSQLServerManagementStudio(管理员) 文件(F)编辑(E)视图(M)调试(D)工具(T)窗口(W)帮 .新建查询(N) 对象资源管理器 46 -201 SKY-20170310 连接(C).. 数据库 断开连接(D) 安全性 注册(G).. 服务器对象 新建查询(Q) 复制 AlwaysOn 活动和监视器(M) 管理 启动(S) Integratior 停止(T) SQLServe 暂停(U) 继续(E) 重新启动(A) 策略(O) 方面(A) 启动PowerShell(H) 报表(P) 刷新(F) 属性(R)

图 2-27 通过 SQL Server Management Studio 启动 SQL Server 2012 服务

服务 控制面板系统和安全 帮助(H) 文件(F) 操作(A) 查看(V) 文件(F) 编辑(E) 工具() 帮助(H) 查看(V) 回 打开 组织 刻录 服务(本地) 服务(本地) 名称 ☆收藏夹 名称 描述 状态 启动关型 SQL SerVer (MSSQLSERVER) isCSI发起程序 Smart Card Removal Policy 手动 允许.. Windows Pow 桌面 停止此服务 SNMPTrap 接收... 手动 Windows内存 遇最近访问的位置 暂停此服务 OSoftware Protection 启用... 自动延迟. 显 本地安全策略 重启动此服务 SPP Notification Service 提供. 手动 打印管理 向库 O SQL Full-text Filter Daemon Launcher (MS... 手动 已启动 Servi... 服务 视频 描述： 恭SQLServer (MSSQLSERVER) 自动 高级安全Wind 提供数据的存储、处理和受控访问， 启动(S) 国图片 O SQL Server Analysis Services 自动 计算机管理 并提供快速的事务处理。 停止(0) 国文档 SQLServer Browser 禁用 任务计划程序 暂停(U) SQL Server Distributed Replay 迅雷下载 手动 事件查看器 恢复(M) SQL Server Distributed Replay 音乐 手动 数据源(ODBC) 重新启动(E) SQL Server Integration Service 自动 图系统配置 SQL Server Reporting Service 自动 性能监视器 所有任务(K) 家庭组 SQL ServerVSSWriter 自动 窗组件服务 刷新(F) SQLServer代理(MSSQLSERV 手动 计算机 SSDPDiscovery 启动 属性(R) 手动 酱本地磁盘 (C:) Superfetch 自动 帮助(H) 本地磁盘 (D:) System Event Notification Serl 启动 自动 本地磁盘 (E:) OTablet PC Input Service 启用... 手动 DVDRW驱动器 扩展人标准 服务 修改日期：2009/7/1412:54 25% 快捷方式 大小1.25KB

图 2-28 通过“服务”窗口启动SQLServer 2012 服务

### 3．验证系统数据库

SQL Server 2012 安装后，由安装程序自动创建了4 个系统数据库，样本数据库则不会 自动安装，若需要可以单独安装。在 SQL Server Management Studio 窗口中单击服务器下 的“数据库”节点，可以看到自动创建的系统数据库，如图2-29所示。 MicrosoftSQLServerManagementStudio(管理员) 文件(E)编辑(E)视图(V 窗口W 调试(D) 工具口 .新建查询(N) 对象资源管理器 连接 $SKY-20170310IRL(SQLServer11.0.3128 数据库 系统数据库 master model msdb tempdb 数据库快照 ReportServer ReportServerTempDB 安全性 服务器对象 AlwaysOn高可用性 管理 IntegrationServices目录 SQLServer代理(已禁用代理XP)

就绪

图 2-29 通过 SQL Server Management Studio 查看 SQL Server 2012 系统数据库

VMSSQL\DATA”打开 DATA文件夹，可以看到系统自动创建的数据库数据文件和日志文 件，如图2-30所示。

《ProgramFilesMicrosoftSQLServerMSSQL11.MSSQLSERVERMSSQLDATA 搜素DATA 帮助(H) 文件(日) 编辑(E) 工具 查看M 新建文件夹 共享 刻录 组织 包含到库中一 大小 Microsoft SQL Server 名称 类型 修改日期 80 master SQL Server Data.. 2017/3/12 19:09 4,992 KB 90 mastlog SQL Server Data.. 2017/3/12 19:09 1,792 KB 100 model 4,160KB 2017/3/12 19:09 SQL Server Data.. 110 modellog 2017/3/12 19:09 SQL Server Data.. 1,024 KB MSAS11.MSSQLSERVER 安全证书 MS_AgentSigningCertificate 1 KB 2017/3/1219:03 MSDBData 2017/3/12 19:09 MSRS11.MSSQLSERVER SQL Server Data... 17,088 KB 选择要预览 MSDBLog 2017/3/1219:09 SQL Server Data.. 20,096 KB 4MSSQL11.MSSQLSERVER 的文件。 5,184 KB ReportServer 2017/3/12 19:09 SQL Server Data... MSSQL ReportServer_log 7,040 KB SQL Server Data... 2017/3/12 19:09 Backup SQL Server Data... ReportServerTempDB 2017/3/12 19:09 4,160 KB Binn ReportServerTempDB_log 1,040 KB 2017/3/12 19:09 SQL Server Data... DATA 甲 tempdb SQL Server Data... 8,192 KB 2017/3/1219:11 >FTData templog 768 KB SQL Server Data... 2017/3/1219:31 Install 13个对象

图 2-30 在“资源管理器”窗口中查看SQLServer 2012数据库文件 47

### 4.查看目录和文件内容

SQL Server 2o12安装完成后，其目录和相应文件的位置是Program Filesl Microsoft SQL Server，目录结构如图 2-31所示。如果这些文件和目录都存在，则表示系统安装成功

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

计算机本地磁盘（C)ProgramFiles√MicrosoftSQLServer 搜素MicrosoftSQLServer 文件(E) 工具D 编辑(E) (A)指 共享→ 刻录 组织～ 包含到库中 新建文件夹 48 Program Files 修改日期 类型 名称 Adobe 80 文件夹 2017/3/1218:40 Common Files 90 文件夹 2017/3/1218:40 DVD Maker 100 文件夹 2017/3/1218:41 IDT 110 文件夹 2017/3/1218:47 选择要预览的文 Internet Explorer 文件夹 MSAS11.MSSQLSERVER 2017/3/1216:05 件。 Microsoft Analysis Services MSRS11.MSSQLSERVER 文件夹 2017/3/1218:50 文件夹 MSSQL11.MSSQLSERVER 2017/3/1218:49 >MicrosoftGames >Microsoft Help Viewer Microsoft Office Microsoft SQLServer 7个对象

图 2-31 SQL Server 2012 的存储目录结构 其中，80文件夹中包含了与先前版本兼容的信息和工具，90文件夹中主要存储单台 计算机上的所有实例使用的公共文件和信息 打开“安装目录\MSSQL11.MSSQLSERVERVMSSQL”，其包括的各目录文件的含义如下： (1） Backup 备份文件的默认位置。 (2）\Binn—— 可执行文件、联机手册文件和用于扩展存储过程的动态链接库文件的位置。 \DATA一一系统数据库文件和样本数据库文件。 (3) (4) 全文本系统文件。 FTData (5) VInstall一一在安装过程中运行的脚本文件和运行安装脚本文件产生的结果文件。 （6）Wobs一一作业结果文件的存储位置

## (7）Log

错误日志文件。 （8）(Repldata 用于复制操作的工作目录。

## SQL Server 2012 的安全性

### 2.3

所谓数据库系统的安全，是指数据库系统中的数据不被破坏、偷窃和非法使用。因此， 数据库系统的安全性问题是每个数据库系统设计者、管理员都必须认真考虑的问题。SQL Server 2012 为维护数据库系统的安全性提供了完善的管理机制和简单而丰富的操作手段。

## 安全性综述

## SQL Server 2012

### 2.3.1

在 SQL Server 2012 数据库服务器系统中，采用了两级权限的安全性管理机制。第一级 是服务器级的“连接权”；第二级是数据库级的“访问权”。SQL Server 2012运行在微软视 窗操作系统平台下，并且 SQL Server数据库中又包含有很多对象，因此，SQL Server 2ol2 的安全性机制可以划分为以下的4个等级： （1）计算机操作系统的安全性。 （2）SQL Server 2012 的登录安全性。 (3) 数据库的使用安全性。 数据库对象的使用安全性。 (4) 每一级别的安全等级就好像一道闸门，如果门没有关闭上锁，或者用户拥有开门的钥 匙，则用户可以通过这道闻门达到下一个安全等级。如果通过了所有的闸门，则用户就可 以实现对相应数据的访问。

### 1．操作系统级别的验证

在用户使用客户计算机通过网络实现对 SQL Server 服务器的访问时，用户首先要获得 客户计算机操作系统的使用权。一般来说，在能够实现网络互连的前提下，用户没有必要 直接在运行 SQL Server 服务器的主机上进行登录，除非 SQL Server 服务器就运行在本地计 算机上。保证操作系统安全性是操作系统管理员或者网络管理员的任务。由于 SQL Server 采用了与 Windows 集成的网络安全机制，因此使得操作系统的安全性也显得尤为重要，同 时也加大了管理数据库系统安全性和灵活性的难度。

### 2．服务器级别的验证

SQL Server 的服务器级安全性建立在控制服务器登录账户和密码的基础上。SQL Server 采用了标准 SQL Server 登录和集成 Windows 登录两种方式。无论是使用哪种方式登 录，用户在登录时提供的登录账户和密码决定了用户能否获得 SQL Server 的访问权，以及 在获得访问权以后，用户在访问 SQL Server 进程时可以拥有的权利。管理和设计合理的登 录账户是 SQL Server 系统管理员的重要任务。

### 3．数据库级别的验证

在用户通过 SQL Server 服务器的安全性检验以后，将直接面对不同的数据库入口。这 是用户将接受的第三次安全性检验。默认情况下，数据库的所有者可以访问该数据库的对 象，还可以分配访问权给其他用户，以便让其他用户也拥有针对该数据库的访问权力。

### 4．数据库对象级别的验证

数据库对象的安全性是核查用户权限的最后一个安全等级。在创建数据库对象的时 候，SQL Server 将自动把该数据库对象的拥有权赋予该对象的创建者。对象的所有者可以 实现该对象的完全控制。默认情况下，只有数据库的所有者可以在该数据库下进行操作。 当一个非数据库所有者想访问数据库中的对象时，必须事先由数据库的所有者赋予该用户 对指定对象执行特定操作的权限。例如，一个用户想访问“机房计费信息管理”数据库中

## 权限验证模式

### 2.3.2

验证模式指的是安全方面的问题，每一个用户要使用 SQL Server 2012 都必须经过验 证。在安装过程中，系统会提示选择验证模式，也可以在安装完成后根据需要来更改验证 模式，更改方法将在2.4.4 节中的例 2.1 中说明。

### 1．Windows 身份验证模式

49 在该验证模式下，用户对 SQL Server 的访问由 Windows 操作系统对 Windows 账户或 用户组验证完成，SQL Server 2ol2 检测当前使用的 Windows 用户账号，如果 SQL Server 允许通过 Windows 验证模式验证用户，使用 Windows 的用户名和密码就可以成功地连接 SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) 到 SQL Server 数据库服务器。在这种方式下，用户不必提供密码或者登录名给 SQL Server 2012 验证。当登录到 Windows 的用户与 SQL Server 2012 连接时，用户不需要提供 SQL Server 登录账号，就可以直接与 SQL Server 相连。这种登录验证模式要求 SQL Server 系统 50 管理员必须指定哪些Windows 账户和账户组作为有效的登录账号，并同时指定 SQL Server 的安全验证模式为“Windows验证模式”。 与 SQL Server 验证模式相比较，Windows 验证模式具有许多优点，这是因为Windows 验证模式集成了 Windows NT 或 Windows Server 的安全系统，由于基于 NT 核心的安全管 理具有众多特征（如安全合法性、密码加密、对密码最小长度进行限制等），所以当用户试 图登录到 SQL Server 时，它基于NT 核心的服务器平台的网络安全属性中获取登录用户的 账号与密码，并使用该平台的验证账号和密码的机制来检验登录的合法性，Windows 修复 安全漏洞的速度远比 SQL Server 快，所以这种验证模式是比较安全的。

### 2． SQL Server 验证机制

当登录到 Windows 的用户与 SQL Server 连接时，用户必须提供 SQL Server 登录账号 和密码，经过 SQL Server 安全系统对用户的身份进行验证合法后才能够连接数据库。使用 SQL Server 验证机制时，SQL Server 系统管理员必须定义登录账号和密码，并指定 SQL Server工作在 SQL Server验证模式下。

### 3.SQLServer 与 Windows 混合身份验证

混合验证模式（Windows身份验证和 SQL Server身份验证）允许以 SQLServer验证方 式或者Windows 验证方式来进行连接。具体使用哪种方式，则取决于在最初的通信中使用 的网络库。如果一个用户使用 TCP/IP Sockets 进行登录验证，它将使用 SQL Server 验证模 式；如果使用命名管道，登录验证将使用Windows 验证模式。这种登录验证模式可以更好 地适应用户的各种环境，是应用系统开发中最常用的一种方式。

## 数据库用户账号、角色和权限

### 2.3.3

通过上述验证模式连接到 SQLServer数据库后，用户必须使用特定的用户账号才能对 数据库进行访问，而且只能操作经授权后可以操作的表、视图和执行经授权后可执行的存 诸过程及管理功能。

### 1．数据库用户账号

当验证了用户的身份并允许其登录到 SQL Server 之后，用户并没有权限对数据库进行 操作，必须在用户要访问的数据库中设置登录账号并赋予一定的权限。这样做的目的是防 止一个用户在连接到 SQL Server之后，对数据库上的所有数据库进行访问。例如，有两个 数据库 student 和 person，如果只在 student 数据库中创建了用户账号，这个用户只能访问 数据库，而不能访问 person 数据库。 student

### 2．角色

角色是将用户组成一个集体授权的单一单元。SQL Server 为常用的管理工作提供了一 组预定义的服务器角色和数据库角色，以便能够容易地把一组管理权限授予特定的用户。 也可以创建用户自定义的数据库角色。在 SQL Server 中用户可以有多个角色。

### 3．权限的确认

用户连接到 SQL Server之后，对数据库进行的每一项操作，都需要对其权限进行确认， SQL Server 采取以下三个步骤来确认权限： （1）当用户执行一项操作时，例如，用户执行了插入一条记录的指令，客户端将用户 的 T-SQL 语句发给 SQL Server。 (2） 当 SQL Server 接收到该命令语句后，立即检查该用户是否有执行这条指令的权限 （3）如果用户具备这个权限，SQLServer 将完成相应的操作，如果用户没有这个权限， SQL Server将返回一个错误给用户。

# SQL Server 2012 工具

### 2.4

SQL Server 2012 是典型的客户机/服务器体系结构的大型系统应用程序。根据各模块 功能的不同，SQL Server 2012提供了不同的服务。对部分主要服务的介绍参见 2.1.2 节的 相关内容。 在诸多服务中，SQL Server 服务是最为重要的一项。SQL Server 2012 通过一套工具集 向数据库管理人员提供了用于配置、管理和使用 SQLServer数据库核心引擎的途径。这些 工具根据功能可以分为： 配置管理工具一一负责与 SQL Server 数据相关的配置工作。 (1) (2) 集成管理平台一一负责与 SQL Server 相关的管理工作。 性能工具一一用于对 SQL Server 数据的性能进行分析。 (3) 商业智能开发平台一一用于商业智能架构应用程序。 (4) (5) 数据库引擎优化顾问工具一一帮助用户分析工作负荷、提出优化建议等。 一用命令行方式对数据库进行管理和操作，如 bcp、dta、osql、sqlserver、 实用工具 (6) Ssms 等，限于篇幅，不再一一赘述，读者可查阅相关资料来了解。

## 配置 SQL Server 2012 服务器

### 2.4.1

要控制 SQL Server 2012 的服务，必须首先配置 SQL Server 2012服务器。可以通过"SQL Server 配置管理器”来配置 SQL Server 2012 服务器。打开 Sql Server Configuration Manager 窗口，如图2-26 所示。在该窗口中可以对 SQL Server 2012 的服务、网络（32/64位）和客

## 户端（32/64位）三项进行配置。

### 1.SQL Server 2012 属性配置

Server 服务”选项，在右窗格中会列出当前计算机上的所有 SQL Server 20l2 服务，并可查 看服务的运行状态、启动模式、登录身份、进程ID、服务类型等状态信息。 右击相应服务，在弹出的快捷菜单中选择“属性”命令，就可以打开该服务的属性窗 口，通过“登录”“服务”、FILESTREAM、“AlwaysOn高可用性”“启动参数”“高级”6 个选项卡对该服务的属性进行配置，如图2-32（a）、（b）、（c）、（d）、（e）、（f）所示。“登 录”选项卡可以更改服务的登录身份，各选项的含义与安装 SQL Server 2012过程相关环节 51 中的选项含义相同。登录身份一旦更改，必须重新启动服务器，更改才能生效。在“服务” 选项卡中可以查看相应服务的详细信息，并可以改变服务的启动模式为“启动”“已禁用” “手动”三种模式之一。FILESTREAM 选项卡可以设置在系统中的 FILESTREAM 启用情 SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) 高可用性”选项卡对该功能的使用进行了简要说明。“启动参数”选项卡 况。“AlwaysOn 显示现有的启动参数，并允许对启动的参数进行设置。“高级”选项卡中是服务的一些高级 属性，一般情况下无须更改。 52 SQLServer(MSSQLSERVER)属性 SQLServer(MSSQLSERVER)属性 登录 服务 AlwaysOn高可用性启动参数高级 服务 FILESTREAM FILESTREAM Alwaysn高可用性启动参数高级 General 登录身份为： SQL服务类型

# SQL Server

①内置帐户(B)： 错误控制 二进制路径 "C:{Program Files),Microsoft SQL 本账户(H)： 进程ID 1384 名称 5QL Server (MSSQLSERVER) 帐户名(N)： NT Service MSSQLSERVER 浏览() 启动模式 自动 密码(A): 退出代码 主机名 SKY-20170310IRL 确认密码(C): 正在运行 状态

服务状态： 正在运行

SQL服务类型

# SQL Server

启动(S) 停止 暂停(D) 重新启动(R) 确定 取消 应用(A) 帮助 确定 取消 帮助 应用(A) (b) (a) SQLServer(MSSQLSERVER)属性 SQLServer(MSSQLSERVER)属性 AlwaysOn高可用性 登录 FILESTREAM 启动参数 服务 登录 服务 AlwaysOn高可用性 高级 FILESTREAM 启动参数 高级 AlwaysOn可用性组功能要求SQLServer2012(或更高版本的 针效Transact-SQL访问启用FILESTREAM(E x86(非Wow)或x64EnterpriseEdition运行在安装了WSFC修补 程序KB2494036的WindowsServer200B（或更高版本)上：此 SQLServer版本和/或WindowsServer系统不满足其中二个或多 启用FILESTREAM进行文件I/O访问(E) 个要求。 有养AlwaysOn可用性组的先决条件、限制和建议的详细信息， Windows共享名(W): MSSQLSERVER 请参阅SQLServer联机丛书。 允许远程客户端访问FILESTREAM数据(R)

取消 帮助 帮助 确定 确定 取消 应用(A) 应用(A) (c) (d) SQLServer(MSSQLSERVER)属性 SQLServer(MSSQLSERVER)属性 启动参数 登录服务 登录服务 FILESTREAM AlwaysOn高可用性 高级 FILESTREAM AlwaysOn高可用性 启动参数 日高级 指定启动参数(S)： ServicePack级别 添加(D) SQL状态 2053 安装路径 C:1(Program Files),Microsoft sQL 现有参数(): 版本

### 11.1.3000.0

-dC: IProgram Files Microsoft SQL Server MSSQL11.MSs 错误报告 eC:\Program Files Microsoft SQL 5erver MSSQL11.MS5 HC:IProgram FilesMicrosoft SQL Server MSSQL11.MSS 单品ID 1804890536 单品名称 Enterprise Edition 客户反馈报告 删除(R) 启动参数 -dC:\Program Files\Microsoft SC 群集 实例ID MSSQL11MSSQLSERVER 数据路径 C:1Program Files)Microsoft SQL 文件版本 2011.110.3128.0 虚拟服务器名称 ServicePack级别 在此SQLServer实例上应用的ServicePack级别，

应用(A) 帮助 取消 帮助 确定 取消 确定 应用(A) (J) (e) 图 2-32 配置 SQL Server 服务的属性 FILESTREAM是在 SQL Server 2008 新引I入的一种存储大容量非结构化数据 (BLOB, 数据类型。存储在 FILESTREAM 列中的 二进制大型对象）的方法，称为 FILESTREAM BOLB 由 SQL Server 操控，数据则驻留在操作系统的文件中，使得定义的 BLOB 对象不再 件的状态都与数据库同步。建议针对 T-SQL访问和文件 IO流启用 FILESTREAM。 AlwaysOn 是 SQL Server 2012 中新增的一个新增高可用性解决方案。在 AlwaysOn 之 前，SQL Server 已经有的高可用性和数据恢复方案，比如数据库镜像、日志传送和故障转 移集群，都有其自身的局限性。而 AlwaysOn 作为微软新推出的解决方案，提取了数据库 镜像和故障转移集群的优点。

### 2．SQL Server 2012 网络配置

在如图 2-26 所示的配置管理器中单击左窗格中的“SQL Server 网络配置”选项下的 “MSSQLSERVER的协议”节点，可以看到当前实例所应用的协议和状态，如图2-33所示。 Sql Server Configuration Manager 文件(E)操作(A)查看(M 帮助(H)

SQL Server配置管理器 (本地) 状态 协议名称 目SQLServer服务 SharedMemory 已启用 具.SQLServer网络配置(32位) 已禁用 NamedPipes 享.SQLNativeClient11.0配置(32位) 已启用 TCP/IP 早.SQLServer网络配置 良MSSQLSERVER的协议 享.SQLNativeClient11.0配置

图 2-33 配置 SQL Server 2012 的网络 SQLServer2012 支持以下协议：

## （1）Shared Memory（共享内存）

客户机和服务器在本地通过共享的内存进行连接。 （2）Named Pipes（命名管道）一一命名管道是一种简单的进程间通信机制，是两个程 序（或计算机）之间传送信息的管道。当建立此管道之后，SQL Server随时都会等待此管 道中是否有数据包传递过来等待处理，然后再通过此管道传输相应数据包。Windows 服务 器都使用 Named Pipes 来相互通信，SQL Server 2012 也同样如此。所有微软的客户端操作 系统都具有通过 Named Pipes 与 SQL Server 2012 进行通信的能力。因为在安装过程中需要 Named Pipes，如果在安装时删除了Named Pipes，安装过程就会失败。因此，只能在安装 后才能册删除 Named Pipes。本地命名管道以内核模式运行，速度会非常快。 (3） TCP/IP—— 客户机和服务器之间采用IP地址和服务端口进行连接。如果端口号使 月 TCP/IP 与服务器连接时，在服务器端的 TCP/IP 端口号也必须为 用1433，则用户端要用 1433。此外，如果设置代理服务器，则也可让 SQLServer 与此代理服务器连接，并在代理 服务器地址栏中输入代理服务器的 IP 地址。网络速度快时，TCP/IP 客户端与命名管道客 户端性能不相上下，但网络速度越慢，二者的差距就越明显 53 右击相应协议，通过弹出的快捷菜单中的命令可以启用或禁用该协议，配置该协议的 属性。

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

### 3．配置 SQL Server 2012客户端

在如图2-26所示的配置管理器中展开左窗格中的“SQL Native Client 10.0配置（32位）” 选项，单击相应部分可以配置 SQLServer 2012客户端协议，如启用、禁用、设置协议顺序 54 等，以及根据协议设置一个预定义的客户端和服务器之间连接的别名。

# 注册和连接 SQL Server 2012 服务器

### 2.4.2

配置完成后，就可以用管理工具管理 SQLServer 服务器上的服务了。最常用的工具是 SQL Server Management Studio（SSMS）。为了可以在管理工具中管理好多个不同的服务器 实例，需要在管理工具中注册服务器，以便对服务器实例进行更好的监控和管理。

### 1．SQL Server 2012 数据库服务器的注册

选择“开始”→“所有程序”→Microsoft SQL Server 2o12→SQL Server Management Studio 命令，打开如图2-34 所示的“连接到服务器”对话框。 连接到服务器 Microsoft

## SQLServer2012

数据库引擎 服务器类型(T): SKY-20170310IRL 服务器名称(S)： Windows身份验证 身份验证(A)： SKI20170310IRLLAdministrator 用户名()： 密码()： 记住密码组）

帮助 连接(C) 取消 选项()》

SQL Server Management Studio 的“连接到服务器”对话框 图 2-34 单击“取消"按钮，打开如图 2-35 所示的无服务器连接的 SQL Server Management Studio 窗口。在“已注册的服务器”窗格中没有任何数据库服务器。其工具栏中的4个图标代表 不同的服务器类型，单击其中一个图标可以确定要注册的新服务器的类型。 对象资源管理器-MicrosoftSQLServerManage.. 文件(F)编辑(E)视图(V)工具(T)窗口(W) 帮助(H) .新建查询(N) 已注册的服务器 数据库引擎 本地服务器组 新建查询(Q) 中央管理 对象资源管理器(E) 评估策略V).. 导入策略()... 对象资源管理器 新建服务器组(G)... 连接 新建服务器注册(S)... 任务(T)

就绪 图 2-35 SQL ServerManagement Studio 的无服务器连接窗口 右击“已注册的服务器”窗格中的“数据库引擎”下的“本地服务器组”，在弹出的 “，“， 所示。 新建服务器注册 常规 连接属性 登录 键入服务器名称或从下拉列表中选择服务器名称。 服务器类型(D: 数据库引擎 服务器名称(S): SKY-20170310IRL 身份验证(A): Windows身份验证 用户名(U): SKY-20170310IRL\Administr 密码(P): 记住密码(M) 已注册的服务器 您可以用新名称和服务器说明(可选替换已注册的服务器名称。 已注册的服务器名称(N)： SKY-20170310IRL 已注册的服务器说明(D)：

帮助 测试(E) 取消 保存M

图 2-36 “新建服务器注册”对话框 在该对话框中选择正确的服务器名称和身份验证方式，并进行相应的连接属性设置， 单击“测试”按钮，可以测试与服务器是否成功连接，若成功，则打开如图2-37所示的对 话框，表示注册成功。单击“确定”按钮，返回如图2-36所示的“新建服务器注册”对话 框，单击“保存”按钮，确定注册，在 SQL Server Management Studio 窗口中会出现新注 册成功的服务器图标，如图2-38 所示。 新建服务器注册 连接测试成功。

确定

图 2-37 与服务器连接测试成功

### 2．SQL Server 2012 注册服务器的删除

右击要删除的已注册服务器，在弹出的快捷菜单中选择“删除”命令即可。

### 3．连接 SQLServer 2012 服务器

在如图2-39所示的“对象资源管理器”窗口单击其工具栏中的“连接”按钮，在下拉 55 菜单中选择要连接的服务器类型（如数据库引擎），或单击 “连接”按钮右侧的“连接” 图标，打开如图2-34所示的“连接到服务器”对话框，根据要连接的服务器在注册时设置

SQL Server 2012 综述 (SQL Server 2012)

## 数据库原理与技术

的信息，正确选择服务器类型、服务器名称和身份验证模式。单击“选项”按钮，可以根 据需要，在如图2-40所示的“连接属性”选项卡中配置连接数据库的相关属性。 对象资源管理器-MicrosoftSQLServerManage... 56 工具口 帮助(H) 文件(E) 编辑(E) 窗口W 新建查询（N) 已注册的服务器 对象资源管理器-MicrosoftSQLServerManagem. 数据库引擎 帮助(H) 文件(F)编辑（E)视图（V)调试(D）工具(T)窗口(W) 本地服务器组 新建查询（N） SKY-20170310IRL 中央管理服务器 对象资源管理器 连接~ 数据库引擎(D)... 对象资源管理器X Analysis Services(A)... Integration Services()... 连接 Reporting Services(R)... Azure存储系统(Z).

就绪 就绪 图 2-38 图 2-39 在“对象资源管理器 注册了新服务器的 SQLServer Management Studio 窗 中连接服务器 日连接到服务器 Microsoft

## SQL Server2012

连接属性 其他连接参数 键入或选择要连接的数据库的名称。 默认值> 连接到数据库也）： 网络 默认值》 网络协议(： 字节 4096 网络数据包大小）： 连接 15 连接超时值（T)： 执行超时值）： 加密连接 选择()... 使用自定义颜色)：

全部重置(R)

帮助 选项)< 取消 连接 (C)

图 2-40 “连接到服务器”的“连接属性”选项卡 Studio窗口中会出现所连接的数据库服务器上的各个数据库实例及各自的数据库对象，如 图 2-41 所示。这时，就可以使用 SQL Server Management Studio 进行管理了。 对象资源管理器详细信息-MicrosoftSQLServerManagementStudio(管理员） 文件(E编辑(E)视图M 工具D窗口W 帮助(H) 新建查询(N)路 对象资源管理器 对象资源管理器详细信息X 搜素 SKY-20170310IRL(SQLServer11.0.3128-SKY-20: SKY-20170310IRL(SQLServer11.0.3128-SKY-20170310IRLVAdm... 数据库 名称 系统数据库 策略运行状态 数据库快照 数据库 ReportServer 安全性 ReportServerTempDB 服务器对象 安全性 口复制 服务器对象 AlwaysOn高可用性 复制 管理 AlwaysOn高可用性 IntegrationServices目录 国管理 SQLServer代理（已禁用.. IntegrationServices目录 SQLServer代理(已禁用代理XP) SKY-20170310IRL (SQLServer11.0.3128 -SKY... 8项 就绪

与注册服务器连接成功的 SQL Server Management Studio 窗口 图 2-41

## 启动和关闭 SQL Server 2012 服务器

### 2.4.3

通常情况下，SQL Server服务器被设置为自动启动模式，在系统启动后，会以Windows 后台服务的形式自动运行。但某些服务器的配置被更改后必须重新启动服务器才能生效， 此时就需要数据库管理员先关闭服务器，再重新启动服务器。这也是数据库管理员的一项 基本管理工作。

### 1.在 SQL Server Management Studio 中关闭和启动服务

选择“开始”→“所有程序”→Microsoft SQL Server 2012→SQL Server Management Studio 命令，成功连接到 SQL Server 2012 数据库服务器后，打开如图 2-4l 所示的Microsoft SQL Server Management Studio 窗口，可以对服务进行各种管理 “，“， 命令即可关闭选中的服务器，并停止相应的服务。服务器关闭后，服务器左侧的图标将带 有红色方框的停止符号。 要启动服务，操作与关闭服务类似，只是在右击要启动的服务器后弹出的快捷菜单中 选择“启动”命令即可。服务器启动后，服务器左侧的图标将带有绿色箭头的运行符号。

### 2．在 SQL Server Configuration Manager 中关闭和启动服务

选择“开始”→“所有程序”→Microsoft SQL Server 2o12→“配置工具”→“SQL Server 配置管理器”命令，打开如图 2-26 所示的 Sql Server Configuration Manager 窗口，可以对 服务进行各种配置和管理 57 在如图2-26 所示的窗口的左窗格中单击“SQL Server 服务”选项，在右侧窗格中右击 要关闭的服务，在弹出的快捷菜单中选择“停止”命令即可关闭选中的服务器，并停止相 应的服务。服务器关闭后，服务器左侧的图标将带有红色方框的停止符号。

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

要启动服务，操作与关闭服务类似，只是在右击要启动的服务器后弹出的快捷菜单中 选择“启动”命令即可。服务器启动后，服务器左侧的图标将带有绿色箭头的运行符号。

# SQL Server 2012 的常用工具

### 2.4.4

58

### 1.SQL Server Management Studio（SSMS，强大的集成管理工具）

Microsoft SQL Server Management Studio 是 Microsoft 为用户提供的可以直接访问和管 理 SQL Server数据库和相关服务的一个新的集成环境。它将图形化工具和多功能的脚本编 辑器组合在一起，完成对 SQL Server 的访问、配置、控制、管理和开发等工作，还能访问 SQL Server 提供的其他外围服务，大大方便了技术人员和数据库管理员对 SQL Server 系统 的各种访问，是管理和访问 SQL Server 数据库服务器的主要工具，也是最重要的工具。 正常启动SQLServer数据库服务之后，用户可以通过选择“开始”→“所有程序”→ Microsoft SQL Server 2ol2→Microsoft SQL Server Management Studio 命令启动该集成管理 环境，在成功连接到数据库服务器后，其窗口基本结构如图 2-4l 所示。连接 SQL Server 数据库服务器的操作可以参考 2.4.2节的相关内容。 由图2-41 可以看出，SSMS 窗口中集成了多个管理和开发工具，默认情况下由“对象 资源管理器”窗格和“对象资源管理器详细信息”窗格两部分组成，有的情况下也显示“已 注册的服务器”窗格。另外，SSMS 窗口还提供了“查询编辑器”“模板资源管理器”“解 决方案资源管理器”等管理窗格或面板。要显示或隐藏某个管理工具的窗格或面板，可以 选择“查看”菜单中相应的命令来实现。 1）已注册的服务器

理器的左侧（也可将其作为右侧的选项页）。在该窗格中可以查看已经注册到本集成管理环 境的各类 SQL Server 服务器的情况。主要通过该管理工具来注册新的 SQL Server 服务器、 删除已经注册的 SQL Server 服务器，以及将服务器组合成逻辑组。具体操作可以参见 2.4.2 节的相关内容。也可以用它来启动和关闭 SQL Server 服务器，设置 SQL Server 服务器的属 性，将已注册的服务器连接到对象资源管理器。 2）对象资源管理器 “对象资源管理器”窗格位于集成管理器的左侧。该管理工具的功能类似 SQL Server 以前版本的 SQL Server Enterprise Manager 工具，所以主要的管理工作是通过“对象资源管 理器”窗格来完成的。 “对象资源管理器”窗格以树状结构组织和管理数据库实例中的所有对象。可依次展 开根目录，用户选择不同的数据库对象，该对象所包含的内容会出现在右边的“详细信息” 窗格中，“详细信息”窗格中的工具栏会做相应的调整，保持其提供的操作功能与被操作对 象所允许的操作一致。用户可以通过选择对象，单击“详细信息”窗格的工具栏中的按钮 来执行操作，也可以通过右击要操作的数据库对象，在弹出的快捷菜单中选择相应的命令 来完成。 数据库对象主要有：

## SQL Server 2012

（1）表一一数据库存放数据的基本单位，具有一定的结构，是创建其他数据库对象的 基础。 （2）视图一一存储的查询，即虚拟表，用表格的形式将数据库中表内的数据按需要组 合集中起来，方便数据访问，对数据进行保护，是数据库的模式映射到外模式的一种实现方法。

能，帮助用户访问到数据库表中的特定信息，但在总体上会增加数据库的负担。 （4）函数一一由系统提供或用户自定义地用于执行特定操作的 SQL语句和可选控制流语 句的预编译集合，是接收参数、执行操作并有返回值的例程。使用函数可以简化数据操纵， 方便应用系统开发。 （5）存储过程 一一由过程化语言编写，经编译和优化后存储在数据库服务器中的过程， 可通过应用程序来调用，极大地简化了数据库管理，方便开发人员设计出更加灵活的应用 系统。 触发器一一是一种特殊的存储过程，当触发事件发生时由系统触发执行，比数据 (6) 库本身标准的功能有更精准和更复杂的数据控制能力，是实现数据完整性的一种强有力手段。 （7）约束一一定义关于字段中允许值的规则，是强制完整性的标准机制。 用对象资源管理器工具主要可以完成的操作有： （1）启动、暂停或停止 SQL Server 服务。 (2) 配置服务器属性。 在“对象资源管理器”窗格中右击数据库服务器名称，在弹出的快捷菜单中选择“属 性”命令，打开如图2-42所示的“服务器属性”对话框，显示和设置 SQL Server 2012服 务器属性。选择左窗格中的目录项，可以在右窗格中查看和设置相应的信息。例如，选择 “常规”选项可以查看 SQL Server 2012 的系统配置，也可以选择其他目录项查看或修改服 务器设置、数据库设置、安全性、连接特性等，以提高数据库服务器系统的性能。 服务器属性-SKY-20170310IRL 选择页 写脚本眉帮助 内存 处理器 安全性 名称 连接 SKI20170310IRL 产品 Microsoft SQL Server Enterprise (64-bit) 数据库设置 操作系统 Microsoft Windows NT 6.1 (7601) 平台 权限 T x64 版本

### 11.0.3128.0

语言 中文（简体，中国) 内存 7991 (MB) 处理器 根目录 C: Program FilesuMierosoft SQL ServeriMS 服务器排序规则 Chinese_PRC_CI_AS False 已群集化 启用HADR False

连接 服务器： SKY-20170310IRL 连接： 名称 SKY-20170310IRL/Administrat 服务器和实例的名称。 查看连接属性 更改服务器的属性和设置可能会影响此SQLServer实例的性能安全性和可用 进度 性。改乏前，请先查阅产品文档。 就绪

59 确定 取消

“服务器属性”对话框 图 2-42

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012) 如何使用 SQL Server“对象资源管理器”窗格设置 SQL Server 的验证模式? 【例2.1】 操作步骤如下： （1）如上所述的方法，打开如图2-42所示的“服务器属性”对话框。 60 （2）在“服务器属性”对话框中选择“安全性”选项，如图2-43所示。 设置所需要的“服务器身份验证”“登录审核”以及相应的“服务器代理账户” (3) 单击“确定”按钮，并重新启动 SQL Server 2012数据库服务器即可生效。 (4) 目服务器属性-SKY-20170310IRL 选择页 写脚本眉帮助 图常规 内存 处理器 服务器身份验证 安全性 连接 indows身份验证模式） 数据库设置 SQLServer和windows身份验证模式(S） 高级 权限 登录审核 仅限失败的登录) 仅限成功的登录) ①失败和成功的登录） 服务器代理帐户 启用服务器代理帐户) 代理帐户()： 连接 密码(： *冰冰* 服务器： SKY-20170310IRL 选项 连接： 符合启用通用条件） SKY-20170310IRL/Administrat 启用C2审核跟踪E） 婴查看连接属性 跨数据库所有权链接（C） 进度 就绪

确定 取消

图 2-43 服务器属性的安全性设置 创建、操作和管理数据库、表、视图、存储过程、触发器、索引、用户定义数据类 型和函数等数据库对象。 创建全文索引、数据库图表。 生成 T-SQL 对象创建脚本。 编写、执行和调试T-SQL语句等。 创建、管理用户账户。 【例2.2】 SQL Server 2012 的 sa 密码的设定。 SQL Server 2012 在安装时，数据库系统超级管理员 sa 账号可能未设密码，为安全起 见，需要为 sa账号设定密码，以防止非法的访问连接，避免造成不必要的系统损失。修改 密码可以通过“对象资源管理器”窗格按以下步骤来实现： （1）在“对象资源管理器”窗格中展开根目录，单击“安全性”文件夹中的“登录名” 节点，在右窗格的“摘要”窗格中就会显示出登录账号的列表。 （2）右击sa 账号，在如图2-44 所示的快捷菜单中选择“属性”命令，打开如图2-45 所示的“登录属性”对话框。在“密码”文本框中输入sa的新密码，再在“确认密码”文 本框中输入新密码以保证修改的密码有效。 对象资源管理器详细信息·MicrosoftSQLServerManagementStudio(管理员) 文件[E)编辑(E)视图V) 工具（D窗口W） 帮助(H) 新建查询N密a路 对象资源管理器 对象资源管理器洋细信息X 搜素 SKY-20170310IRL (SQLServer11.0.3128-SKY-20: SKY-20170310IRL (SQL Server 11.0.3128 - SKY-20170310IRLVAdm.. 日数据库 名称 创建日期 国系统数据库 数据库快照 ##MS_PolicyEventProce... 2017/3/12 19:03 ReportServer &,##MS_PolicyTsqlExecut... 2012/2/10 21:07 ReportServerTempDB &NT AUTHORITYSYSTEM 2017/3/12 19:02 安全性 & NT Service\MSSQLSERV... 2017/3/12 19:02 登录名 NT SERVICE\ReportSer... 2017/3/12 19:02 服务器角色 NT SERVICEISQLSERVE... 2017/3/12 19:02 口凭据 & NT SERVICEISQLWriter 2017/3/12 19:02 口加密提供程序 & NT SERVICE\Winmgmt 2017/3/12 19:02 审核 新建登录名(N). 口服务器审核规范 &SKY-20170310IRLVA 编写登录脚本为(S) 服务器对象 田 白 复制 策略(0) 围AlviaysOn高可用性 方面(A) 启动PowerShell(H) 围IntegrationServices目录 SQLServer代理(已禁用代理XP) 报表(P) 重命名(M) 删除(D) 刷新(F) 属性 (R) 就绪

图 2-44 登录账号列表

目登录属性·sa 选择页 写脚本帮助 图常规 雪服务器角色 登录名： 搜索包).. 图用户映射 5a 状态 O置indows身份验证） SQLServer身份验证(S） 密码 (): 确认密码(C)： 指定旧密码 旧密码 (): 强制实施密码策略） 回强制密码过期凶 口用户在下次登录时必须更改密码） O映射到证书(R) ①映射到非对称密钥） 映射到凭据(M) 添加() 连接 映射的凭据 提供程序 凭据 服务器： SKY20170310IRL 连接： SKY-20170310IRLAAdministrat 查看连接属性 进度 删除() 就绪 master 默认数据库也）： Simplified Chinese 默认语言(G)： 确定 取消

图 2-45 在“登录属性”对话框中修改sa账号密码 61 （3）单击“确定”按钮就可以生效 管理数据库对象权限和登录安全性。 配置和管理复制。

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

监视服务器活动、查看系统日志。 备份数据库和事务日志。 导入和导出数据。 62 创建和安排作业。 网页发布和管理。 3）查询编辑器 SQL Server 2012 的 SQL 查询编辑器是以前版本中的 Query Analyzer 工具的替代品，是 一种功能强大的可以交互执行 SQL 语句和脚本 GUI 的管理与图形编程工具，它最基本的 功能是编辑 T-SQL 命令，然后发送到服务器并显示从服务器返回的结果。与 Query Analyzer 总是工作在连接模式下不同，查询编辑器既可以工作在连接模式下，也可以工作在断开模 式下。另外，查询编辑器还支持彩色代码关键字、可视化语法错误显示、允许开发人员运 行和诊断代码等功能，集成性和灵活性有很大的提高。查询编辑器具有以下的主要功能： （1）在查询编辑器中创建查询和其他 SQL 命令并针对 SQL Server 数据库来分析和执 存到报表文件中或导出到指定文件中，可以用Excel打开结构文件并进行编辑和打印。 利用模板功能，可以借助预定义脚本来快速创建数据库和数据库对象等。 (2) (3) 利用对象浏览器脚本功能，快速复制现有数据库对象。 在参数未知的情况下执行存储过程也可以用于调试所编写的存储过程。 (4) (5) 调试查询性能问题，包括显示执行计划、服务器跟踪、客户统计、索引优化向导。 （6）在“打开表”窗口中快速插入、更新或删除表中的行，即对记录进行数据操纵。 ，中口““，中“，口SWSS 编辑”窗格。在其空白编辑区中输入T-SQL命令，单击“面板”工具栏中的“执行”按钮， T-SQL命令的运行结果就显示在“查询编辑器”窗格的下面的“结果”窗格中，如图2-46 所示。用户也可以打开一个含有SQL语句的文件来执行，执行的结果同样显示在“结果” 窗格中。 SQLQuery1.sql- SKY-20170310IRL.master (SKY- 310IRL\Administrator [56))*-MicrosoftSQLServerManagement Studio(管理员) 帮助(H) 文件(E) 窗口W 视图M 编辑(E) 查询（Q） 项目（P) 调试(D) 新建查询(N) master 调试(D) 执行区) 对象资源管理器 SQLQuery1.sql - S..ministrator (56)*X use mastor 当前连接参数 go SKY-20170310IRL(SQLServer11.0.3128-SKY-20: Eselect* 数据库 from spt_values 聚合状态 go 安全性 2515 返回的行数 登录名 结束时间 2017/3/1221:05:2 服务器角色 开始时间 2017/3/12 21:05:28 凭据 连接失败 加密提供程序 名称 SKY-20170310IRL 审核 00:00:00.312 占用时间 100 % 服务器审核规范 打开 状态 结果 消息 连接 服务器对象 连接名称 SKY-20170310IRL 复制 number high 1ow status name type 连接详细信息 AlwaysOn高可用性 HULL HULL rpe SPID 56 管理 HULL HULL pub SKY-20170310IRLV 登录名 IntegrationServices录 sub HULL HULL 返回的连接行数 2515 图SQLServer代理(已禁用代理XP) HULL HULL dist 服务器版本

### 11.0.3128

dpub 16 HULL HULL 名称 NULI 连接的名称， 2515行 SKY-20170310IRLVAdmini. 00:00:00 master

图 2-46 查询编辑器的使用 在“查询编辑器”窗格中，可以控制查询结果的显示方式。T-SQL语句的执行结果能 以文本方式、表格方式显示，还可以保存到文件中。要切换结果显示方式，可以单击“面 板”工具栏中的相应按钮，或在编辑区的快捷菜单中选择所需要的结果显示方式。 如果想获得一个空白的“查询”窗格，以便执行其他的SQL程序，可以单击“标准” ，中‘“，）“，中 件”→“新建”命令），即可新建一个编辑窗口。 输入的SQL语句可以保存成文件，以便重复使用。保存时，将光标定位在编辑窗口中， 然后单击“标准”工具栏中的“保存”按钮（或选择菜单栏中的“文件”→“保存”命令） 即可。查询的结果也可以保存成文件，以便日后查看。保存时，将光标定位在“结果”窗 格中，后续操作与SQL语句的保存方法相同，不同之处是文件的扩展名不同，采用默认的 扩展名即可，以上两种文件都可在 Word等文字处理软件中打开并处理。 4）模板资源管理器 模板资源管理器为数据库管理和开发人员提供了执行常用操作的模板。用户可以在此 模板的基础上编写符合自己要求的脚本，使得各种数据库操作变得更加简洁和方便。 【例2.3】 使用数据库模板创建数据库。 °‘“器，“，（） （2）单击模板中的Database 节点，展开 create database 子节点，双击后连接到数据库， 并在一个新的查询编辑器中给出用于创建一个数据库的 T-SQL脚本模板，如图 2-48 所示。 用户根据需要对该模板进行具体的修改，即可快速创建一个数据库对象。 模板浏览器 Audit Backup SQLQuery2.sql -S...ministrator (54))X SQLQuery1.sql-S...ministrator (56)* Certificate ChangeDataCapture Create database template Change Tracking Credential USE master GO BDatabase Attach Database Drop the database if it already exists Bring Database Online IF EXISTS( E Create Database on Multiple Filegro SELECT name FRoM sys.databases CreateDatabaseSnapshot WHERE name =N<Database_Name, sysname, Database_Name>" Create Database with Filestream File Create Database DROP DATABASE<Database_Name,sysname,Database_Name> E Detach Database GO DropDatabase CREATE DATABASE <Database_Name,sysname,Database_Name) Take Database Offline GO Database Mail 最近使用的模板 100 % 图 2-47 图 2-48 创建数据库的 T-SQL模板 模板资源管理器 5）解决方案资源管理器 解决方案资源管理器主要用于管理与一个脚本工程相关的所有项目，将在逻辑上同属 一种应用处理的各种类型的脚本组织在一起，可以更好地对属于同一应用的各个脚本进行 63 管理和维护。 6） SQL Server Profiler SQL Server Profiler 是用于从服务器中捕获 SQL Server 2012 事件的工具，例如，连接

SQL Server 2012 综述

## 数据库原理与技术

(SOL Server 2012)

服务器、登录系统、执行T-SQL语句等操作。这些事件被保存在一个跟踪文件中，以便日 后对该文件进行分析或用来重播指定的系列步骤，从而有效地发现系统中性能比较差的查 询语句等相关问题 64 7）数据库引擎优化顾问 数据库引擎优化顾问可以帮助用户分析工作负荷、提出创建高效率索引的建议等功 能。用户不必详细了解数据库的结构就可以选择和创建最佳的索引、索引视图、分区等。

### 2．配置工具

（SQLServer Configuration Manager）用于配置 SQL Server服务和网络连接。 配置管理器 SQL Server 2012 是由一系列服务组成的，核心部件Database Engine（数据库引擎）对 应的是 SQL Server 2012 提供的 SQL Server 服务。除此之外，围绕此服务还有一系列相关 的外围辅助服务： （1）Service Broker 服务。

## （2）Replication（复制服务）。

（3）Full-Text（全文索引服务）。 （4）Notification Services（通知服务）。

## （5）Reporting Services（报表服务）。

（6）Analysis Services（分析服务）。 （7）SQL Server Configuration Manager 可以管理上述的大部分服务，使用方法参见

### 2.4.1 节。

### 3. SQLCMD 工具

以上介绍的SSMS与配置工具为数据管理和开发人员提供了功能强大的图形化管理界 面。除此之外,MS SQL Server 2012 服务器还支持用命令行方式进行数据库管理和访问的功能。 在Windows开始菜单中通过“运行”命令执行cmd，进入命令行执行环境。在“命令 提示符”后输入命令“SQLCMD/？”，按 Enter 键，将显示与 SQLCMD 命令使用方法相关 的信息，包括命令的使用格式、各参数的含义、参数使用方法等，如图2-49所示。 c管理员:C:\Windows|system32,CMD.exe C:WsersAdministrator.SKY-2@173i@1RL>sqlcmd/? Microsoft（R）SqLServer命令行工具 版本11.0.2100.60NTx64 版权所有<c）2012Hicrosoft。保留所有权利。 用法：Sglcmd [-P密码] [-U登录 ID] 服务 [-H.机名】 [-E可信连接】 象超时值1 [-t查询超时值] 用数据库名称］［-1 列分隔符 [-w屏幕宽度]］ [-S 据包太小 [-e回显输入 [-1允许带引号的标识符] [-Lc】"出服务器{清除输出] 命令结束 “命令行查询"】 【-Q“命行查询”并退出］ 错误级别 [-严重级别] ［-W删除尾随空格】 icode,输出] [-r[0!1]发送到stdeFr的消息] [-o输出文件］ 输入文件1 [-2新密码] <代码贡>！i:<代码页>，0:<代码页>1]【-z新建密码并退出】 -k[112].册除[换控制字符] 度类型显示宽度 打印统计信息宣号格式1 户端区域设置 子网故障转移1 出错时中止批处理1 ，［-A专用管理连接] -X[行禁用命令 、启动脚本、环境变量[并退出1] 变量替换 C:WsersAdministrator.SKY-20i70310IRL>

图 2-49 SQLCMD命令使用方法 回车后进入 SQLCMD环境,如图 2-50 所示。命令中的参数-U和-P指定登录 SQL SerVer 2012 服务器的合法账号合密码，-S 指定登录的 SQL Server 2012 服务器名。在执行此命令 前，需要对身份验证模式、登录账号和密码进行设置，并确认要登录的 SQL Server 2012 服务器名。在信任连接的情况下，可以省略命令后的参数。 4SQLCMD Microsoftwindows[版本6.1.7601】 版权所有《c）2009MicrosoftCorporation。保留所有权利。 C:NUsersAdministrator.sKY-20170310IRL>sqlcmd-Usa-P123456-ssky-20170310irl

图 2-50 SQLCMD 命令环境 在 SQLCMD 环境中，可以执行T-SQL语句、存储过程、脚本文件等。 【例2.4】 在 SQLCMD环境中查询当前数据库服务器中存在的所有数据库。 在 SQLCMD环境中输入如下 T-SQL语句: USE MASTER SELECT name,create date FROM sys.databases GO 按 Enter 键执行语句，其结果如图 2-51 所示。 - SQLCMD 1>USEMASTER 2>SELECTname,create_date 3>FROM sys.databases 4>.90 已将数据库上下文更改为 'master name create_date master 2003-04-08 09:13:36.390 tempdh 2017-03-1221:18:36.423 model 2003-04-08 09:13:36.390 msdb 2012-02-1021:02:17.770 ReportServer 2017-03-1219:02:21.747 ReportServerTempDB 2017-03-1219:02:22.837 <6行受影响》 1>

图 2-51 SQLCMD命令环境 执行exit 命令则可以退出 SQLCMD环境。 65

### 4．文档和教程

MS SQL Server 2012 具有一套非常完整的联机帮助文档 (SQL Server Books OnLine, BOL），也是 SQL Server 数据库系统的子系统。它为用户提供了完整的 SQL Server 参考文

SQL Server 2012 综述 (SOL Server 2012)

## 数据库原理与技术

档，便于 SQL Server 数据库的使用者根据需要进行查询和检索。联机帮助可以访问本地的 文档，也可访问网络的文档，在网络通畅的情况下，联机访问网络文档会获得较全面的 信息。 66 打开BOL 的方法多种多样，用户可以通过选择“开始”→“所有程序”→Microsoft SQL

令动态地打开并启用BOL功能，如图2-52 所示。 微软正-mhttps://msdn.microsoft.com/zh-cn/library/bb500430-→c× mSQLServer2012安装快... Microsoft DeveloperNetwork MSDN订阅 聚取工具 下载计划社区文档 >产品文档SQLServer2012联机丛书>入门(SQLServer2012） 昌 打印 SQLServer2012的产品规格 要查看英语原文，请勾选“英语”复选框。也可将鼠标指针移到 (0) 胎业 翻译 英语 文本上，在弹出窗口中显示英语原文。 SQLServer2012中的新增功能 SQLServer2012安装快速入门 SQL Server 2012安装快速入门 SQLServer的产品文档入门 本文内容 SQLServer2012/其他版本 Getting Assistance SQLServer安装 向后兼容性 简介 相关任务 关于SQLServer许可条款 SQLServer安装向导基于WindowsInstaller。它提供了一个功能树以用来安装以下SQLServer 相关内容 组件： 请参阅 MicrosoftSQLServer隐私声明 ·数据库引擎 SQLServerWindows微徽标认证 • Analysis Services 卸载后保留的SQLServer文件 Reporting Services

SQL Server 联机丛书 图 2-52 MS SQL Server 2012 还提供了与 SQL Server 数据库相关的帮助教程，使用者可以通过 这些教程更好、更快地掌握 SQL Server 数据库的管理与使用。在图 2-52 中的列表里找到 “教程”即可打开 SQL Server 教程，如图2-53 所示。 m https://msdn.microsoft.com/zh-cn/library/hh23169s.o c × mSQLServer2012教程 Microsoft Developer Network 登录 MSDN订阅 获取工具 计划社区文档 下载 >SQLServer>SQLServer2012>产品文档 昌 打印 要查看英语原文，请勾选“英语”复选框。也可将鼠标指针移到 () SQLServer2012的开发人员参考 翻译 英语 文本上，在弹出窗口中显示英语原文， 人共享 安装SQLServer2012 SQL Server 2012 教程 SQLServer2012服务文档 本文内容 SQLServer2012教程 SQLServer2012其他版本 【本节内容 Analysis Services 教程 SQLServer2012引入了很多新技术和新功能。我们门提供了三个新的或经过重大更新的教程，帮助悠 快速开始使用SQLServer2012. →Reporting Services教程 我们计划在未来提供更多的教程。同时，您可以继续学习SQLSerYer2008R2教程。在某些情况 Integration Services 敏程 下，您可能会发现SQLServer2012与SQLServer2008R2的用户界面之问存在很小的差异，而教 数据库引擎数程 程必备条件也存在细微的差异。如果教程使用AdventureWorks数据库之一，则应下载和使用SQL Server2012版本。 复制教程 如果您使用的是SQLServer2012服务器，则应已安装了SQLServer2012数据访问按口。为了使教 企业信息告理教程 程正常发挥作用，您需要使用这些访问接口的SQLServer2012示例数据库，或者您需要使用示例数 据库的SQLServer2008R2版本的SQLServer2008R2数据访问接口。 文法律声明

图 2-53 SQL Server 教程 练习题

### 1．简述客户机/服务器处理结构。

### 2．SQLServer 2012 主要有哪些版本？安装企业版的软硬件要求是什么？

### 3．SQLServer 2012 包含哪些主要服务?

### 4．SQL Server 2012 支持哪两种身份验证模式？各有何特点？

### 5．一台计算机上可以安装多少个 SQL Server默认实例服务器？多少个 SQL Server命

名实例服务器？注册后的默认实例服务器和命名实例服务器的名称分别是什么？

### 6．收集 Microsoft 公司在发布 SQL Server 2005/2008/2012 系统时的技术白皮书，研究

和讨论 Microsoft SQL Server 系统功能的演变规律。

### 7．上机安装一次 SQL Server 2012，并取实例名为 test，然后卸载安装的该 SQL Server

2012 实例。

67

SQL Server 2012 综述

# 数据库的基本操作
