#百度贴吧分布式爬虫：用户管理端#
##简介##
这里是KCrawlerManager用户端管理软件（KCrawlerController），该软件的作用是从服务器获取当前在线爬虫信息，监视任务执行，以及创建任务，获取任务结果和数据分析。
由于目前使用的是文件储存任务结果，故必须将任务结果从服务器下载到本地才可以进行分析。

*如果你需要直接分析，可以拷贝/Debug/plugins文件夹，然后直接用python运行插件的main.py即可jx 分析。*

##语言及环境##


C++

Visual Studio 2015
###文件结构###
    Debug:这里面包含了可执行文件以及保证可执行程序可以成功运行的必要文件
    Debug/plugins：这里包含了数据分析插件
    KCrawlerControal：用户管理端源代码



##授权条款：GPL##


![GPL](https://www.gnu.org/graphics/gplv3-127x51.png)
