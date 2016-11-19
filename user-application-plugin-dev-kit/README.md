#百度贴吧分布式爬虫：插件开发包#
##简介##
这里包含了该系统自带的几个插件，以及进行插件再开发所需要的lib


##语言及环境##

Python3.5.1

######建议你安装64位的python，否则可能会出现memory error######
###文件结构###
    lib:开发插件所需要的lib，这里面有一些常用任务结果操作函数（可自定义）
    default-plugins：包含了数据分析模块的几个自带插件（某些插件的lib库已经针对插件做出特别修改）

##第三方库##



[matplotlib](http://matplotlib.org/)：用于对数据进行可视化分析

[numpy](https://pypi.python.org/pypi/numpy)：用于对数据进行可视化分析

[jieba中文分词](https://github.com/fxsjy/jieba)：用于中文分词以及关键字提取
##授权条款：GPL##


![GPL](https://www.gnu.org/graphics/gplv3-127x51.png)

**测试数据下载地址：[http://pan.cuit.edu.cn/share/7FF9yiO5](http://pan.cuit.edu.cn/share/F8qiYiIC) （提取码：cm8p）

###数据分析示例###

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


