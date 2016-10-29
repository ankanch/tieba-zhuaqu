##**贴吧爬虫**##
###**简介**###
该python脚本可以用来抓取指定贴吧的帖子标题和作者及发帖时间等相关信息。
抓取的数据可以用于统计某个词的热度以及对比多个关键词出现的频率。
###**各模块说明**###


* `main.py` ： 程序主逻辑

* `maglib.py`       ： 用来输出分隔符

* `tiebaTitle.py`  ：下载网页，抓取标题的主要模块

* `dataminer.py  `  ：提取关键字，进行统计的主要模块

* `graphicsData.py` ：绘图模块（对matplotlib函数进行初步封装）

###**其它必要库**###

`graphicsData.py` 中绘图使用了[matplotlib 库](http://matplotlib.org/) 安装方法：
    
* Windows：pip matplotlib   
* Debian / Ubuntu : sudo apt-get install python-matplotlib
* Fedora / Redhat : sudo yum install python-matplotlib

`dataminer.py` 中使用了 [jieba中文分词模块](https://github.com/fxsjy/jieba) 安装方法见其GitHub页面：https://github.com/fxsjy/jieba
###**其它**###
（有待补充）


授权条款：GPL

