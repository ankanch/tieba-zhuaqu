#百度贴吧分布式爬虫#
##简介##
该分布式爬虫可以抓取贴吧帖子内容并进行相关分析

该爬虫系统主要由3部分组成：TaskManager任务管理服务器，KCrawlerManager用户端管理软件（KCrawlerController），Cralwer爬虫程序
##语言及环境##

Python3.5.1
C++
Visual Studio 2015
######建议你安装64位的python，否则可能会出现memory error######
###文件结构###
    shareLib:系统组成三部分的共享库，定义报文，网络交互操作
    task-manager：TaskManager任务管理服务器
    tieba-zhuaqu：KCrawler爬虫主体
    user-application：KCrawlerManager用户端管理软件KCrawlerController

##第三方库##



[matplotlib](http://matplotlib.org/)：用于对数据进行可视化分析

[numpy](https://pypi.python.org/pypi/numpy)：用于对数据进行可视化分析

[jieba中文分词](https://github.com/fxsjy/jieba)：用于中文分词以及关键字提取


##开发状态##

开发中...

##授权条款：GPL##


![GPL](https://www.gnu.org/graphics/gplv3-127x51.png)
