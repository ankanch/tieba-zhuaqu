##**贴吧爬虫:数据库版**##
---
###**简介**###
---

###--->**该分支添加了数据库支持**<---###
该python脚本可以用来抓取指定贴吧的帖子标题和作者及发帖时间等相关信息。
抓取的数据可以用于统计某个词的热度以及对比多个关键词出现的频率。
###在你继续往下读之前：###
如果你只是简单的想使用这个软件爬取信息并加以分析，你需要下载本文件夹以及以下文件：

    KCrawlerControal:需要使用这个软件里面的数据分析模块

在开始之前请确认你已经安装python3.5以及后面提到的第三方库。
运行本文件夹中的RunTest.bat即可进行抓取。
在linux-dist文件夹中附带了linux版本，方便你们部署到服务器上，在抓取完毕后，会发送邮件提醒。

###**数据库结构**###
---

**使用该版本的贴吧爬虫，你需要有以下数据库结构**

![](https://github.com/ankanch/tieba-zhuaqu/raw/master/README/datebase_structure.jpg)

###**各模块说明**###
---


* `main.py` ： 程序主逻辑

* `maglib.py`       ： 用来输出分隔符

* `tiebaTitle.py`  ：下载网页，抓取标题的主要模块

* `dataminer.py  `  ：提取关键字，进行统计的主要模块

* `graphicsData.py` ：绘图模块（对matplotlib函数进行初步封装）

###**其它必要库**###
---

`graphicsData.py` 中绘图使用了[matplotlib 库](http://matplotlib.org/) 安装方法：
    
* Windows：pip matplotlib   
* Debian / Ubuntu : sudo apt-get install python-matplotlib
* Fedora / Redhat : sudo yum install python-matplotlib

`dataminer.py` 中使用了 [jieba中文分词模块](https://github.com/fxsjy/jieba) 安装方法见其GitHub页面：https://github.com/fxsjy/jieba


###授权条款：GPL###
---

![](https://camo.githubusercontent.com/0e71b2b50532b8f93538000b46c70a78007d0117/68747470733a2f2f7777772e676e752e6f72672f67726170686963732f67706c76332d3132377835312e706e67)

