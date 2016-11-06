import lib.result_functions_file as RFF
import lib.maglib as MSG
import lib.graphicsData as drawGraphic
import datetime
import numpy

#这个库是用来统计某个词语的频率变化并以折线统计图的形式显示
#这是tieba-zhuaqu项目的用户端基本插件

#该函数是可定义的显示函数（慎用）
#参数说明：word：要统计的词语 scale：时间段（单位：天） datelist：贴吧帖子元数据
def singleWordTF(word,datalist,scale=30):
    #实现解析时间线，获取最小最大时间范围
    begtime,endtime = getTimeDomain(RFF.getDateList())
    print("对比日期范围：",begtime,"->",endtime)
    c = endtime - begtime
    blocks = int(c.days/scale)
    feqlist = []
    timeline = []
    x=0
    #初始化频率数组
    print('>>>>>开始处理.....')
    xdate = begtime
    while x<=blocks:
        feqlist.append(0)
        timeline.append(str(xdate.date()))
        xdate += datetime.timedelta(days=scale)
        x+=1
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in datalist:
        if post[0][0].find(word) > -1:
            titledate = datetime.datetime.strptime(post[0][2], "%Y-%m-%d %H:%M")
            deltadate = titledate - begtime
            feqpos = int(deltadate.days/scale)
            feqlist[feqpos]+=1
        replylist = post[1]
        for reply in replylist:
            if len(reply) < 3:
                continue
            if reply[0].find(word) > -1:
                replydate = datetime.datetime.strptime(reply[2], "%Y-%m-%d %H:%M")
                deltadate = replydate - begtime
                feqpos = int(deltadate.days/scale)
                feqlist[feqpos]+=1
    print('>>>>>处理完成，加载图像中.....')
    print(str(feqlist))
    print(str(timeline),str(feqlist))
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(datalist*len(datalist[0][0][0])))+')',timeline,feqlist,'时间频率图('+ str(begtime) + "->" + str(endtime) +")")
    print('>>>>>图像加载完毕')


#该函数用来返回指定日期的区间的主题帖/回帖数据（用于被显示过去天/月/年的函数调用）
#参数说明： begdate:指定开始日期，enddate:指定结束日期
#返回值：post数据的 list
#       [ [内容,作者,时间],[......],...... ]
def getPostDatebyTimeDomain(begdate,enddate,datalist):
    satisfied = []
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in datalist:
        titledate = datetime.datetime.strptime(post[0][2], "%Y-%m-%d %H:%M")
        if titledate < enddate and titledate > begdate:
            satisfied.append(post[0])
        replylist = post[1]
        for reply in replylist:
            if len(reply) < 3:
                continue
            replydate = datetime.datetime.strptime(reply[2], "%Y-%m-%d %H:%M")
            if replydate > begdate and replydate < enddate:
                satisfied.append(reply)
    return satisfied


#该函数用来显示过去指定天数的词频变化
def showLastDays(word,days):
    begdate,enddate = getTimeDomain(RFF.getDateList())
    begdate = enddate - datetime.timedelta(days=days)
    spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    while x < days: #初始化频率数组
        feqlist.append(0)
        timeline.append(str(xdate.month)+"-"+str(xdate.day))
        xdate += datetime.timedelta(days=1)
        x+=1
    #sposdate：[ [内容,作者,时间],[......],...... ]
    for post in spostdate:
        if post[0].find(word) > -1:
            satpos = (datetime.datetime.strptime(post[2], "%Y-%m-%d %H:%M") - begdate).days
            feqlist[satpos-1]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,'时间频率图('+ str(begdate.date()) + "->" + str(enddate.date()) +")")
    print('>>>>>图像加载完毕')
    

#该函数用来显示过去指定月数的词频变化
def showLastMonths(word,months):
    begdate,enddate = getTimeDomain(RFF.getDateList())
    begdate = enddate - datetime.timedelta(days=months*30)
    spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    while x < months: #初始化频率数组
        feqlist.append(0)
        timeline.append(str(xdate.month)+"月")
        xdate += datetime.timedelta(days=30)
        x+=1
    #sposdate：[ [内容,作者,时间],[......],...... ]
    for post in spostdate:
        if post[0].find(word) > -1:
            satpos = int(((datetime.datetime.strptime(post[2], "%Y-%m-%d %H:%M") - begdate).days)/30)
            feqlist[satpos-1]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,'时间频率图('+ str(begdate.date()) + "->" + str(enddate.date()) +")")
    print('>>>>>图像加载完毕')

#该函数用来显示过去指定年的词频变化
def showLastYears(word,years):
    begdate,enddate = getTimeDomain(RFF.getDateList())
    begdate = enddate - datetime.timedelta(days=years*365)
    spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    print("begdate=",begdate,"enddate=",enddate)
    while x < years: #初始化频率数组
        feqlist.append(0)
        timeline.append(str(xdate.year)+"年")
        print(str(xdate.year))
        xdate += datetime.timedelta(days=365)
        x+=1
    #sposdate：[ [内容,作者,时间],[......],...... ]
    for post in spostdate:
        if post[0].find(word) > -1:
            satpos = int(((datetime.datetime.strptime(post[2], "%Y-%m-%d %H:%M") - begdate).days)/365)
            feqlist[satpos-1]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,'时间频率图('+ str(begdate.year) + "->" + str(enddate.year) +")")
    print('>>>>>图像加载完毕')

#该函数用于从外部执行
def extrenSingleWordTF():
    word = input("请输入要统计的词语：")
    scale = int(input("输入天/月/年："))
    #showLastDays(word,scale)
    #showLastMonths(word,scale)
    showLastYears(word,scale)
    #singleWordTF(word,RFF.getPostDataList(),scale)

#该函数为辅助函数，用于找出时间区间
#返回值：最早时间，最近时间
def getTimeDomain(datelist):
    datelist.sort()
    return datelist[0],datelist[len(datelist)-1] 

#该函数为辅助函数，用于将str转化为datetime对象
#返回值：datetime对象
def toDatetime(datastr):
    return datelist.append(datetime.datetime.strptime(datastr, "%Y-%m-%d %H:%M"))
    

#逻辑
extrenSingleWordTF()