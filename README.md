#百度贴吧分布式爬虫#
---
##简介##
---
该分布式爬虫可以抓取贴吧帖子内容并进行相关数据分析（详情见数据分析示例）。

目前该系统内部自带了4个插件用于数据分析，你可以给它贡献更多插件（插件由Python编写）

该爬虫系统主要由3部分组成：TaskManager任务管理服务器，KCrawlerManager用户端管理软件（KCrawlerController），Cralwer爬虫程序

###在你继续往下读之前：###

如果你只是简单的想使用这个软件爬取信息并加以分析，你需要下载以下文件：

    tieba-zhuaqu：贴吧抓取主程序（请运行RunTest.bat）
    KCrawlerControal:需要使用这个软件里面的数据分析模块

在开始之前请确认你已经安装python3.5以及后面提到的第三方库。

** 注意：你需要将`AttachImport`文件下的`ktieba`文件夹放入C盘根目录，才能够正常运行。

##语言及环境##
---

Python3.5.1

C++

Visual Studio 2015

######建议你安装64位的python，否则可能会出现memory error######

##文件结构##
---

**所有以DSV开头的文件夹代表其对应的数据库版本（Database Support Version）（默认为任务结果文件版本）**

    shareLib:系统组成三部分的共享库，定义报文，网络交互操作
    task-manager：TaskManager任务管理服务器
    tieba-zhuaqu：KCrawler爬虫主体
    user-application：KCrawlerManager用户端管理软件KCrawlerController
    DataAnalyzer：数据分析套件（从user-application中独立出来的）

数据库结构见下图：


![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/datebase_structure.jpg)


##第三方库##
---


[matplotlib](http://matplotlib.org/)：用于对数据进行可视化分析

[numpy](https://pypi.python.org/pypi/numpy)：用于对数据进行可视化分析

[jieba中文分词](https://github.com/fxsjy/jieba)：用于中文分词以及关键字提取

##数据分析模块##
---

**测试数据下载地址：[http://pan.cuit.edu.cn/share/7FF9yiO5](http://pan.cuit.edu.cn/share/F8qiYiIC) （提取码：cm8p）

数据分析示例见文档末尾


##开发状态##
---

开发中...

##授权条款：GPL##
---


![GPL](https://www.gnu.org/graphics/gplv3-127x51.png)



   
###数据分析示例###
---

目前自带的数据分析插件可以完成以下几种类型的分析：

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_1.png)

对比统计多个词语（multiwords）

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_2.png)

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_2-2.png)

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_2-3.png)

显示某个词语的词频-时间图（wordstimeline）


####分析特定用户####

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_3-1.png)

分析某位用户的贴吧活跃度（userX）

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_3-2.png)

分析某位用户的高频关键字（userX）

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/figure_3-3.png)

分析某位用户的贴吧活跃时间段（userX：通过叠加每日活跃时间段）

