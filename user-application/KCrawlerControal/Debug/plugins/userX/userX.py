import lib.result_functions_file as RFF
import lib.maglib as MSG
import lib.graphicsData as drawGraphic
import jieba.analyse
import datetime
import numpy
import os

#KCC基本分析组件
#该组件用于统计某个词语的频率变化并以折线统计图的形式显示

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

#该函数用于找出指定用户的回帖数据 *仅用于处理二级数据
#返回值：post数据 [[内容,时间],[...],...]
def getPostByAuthor(authorname,datalist):
    postData = []
    for post in datalist:
        if post[1] == authorname:
            postData.append(post)
    return postData

#该函数用来显示指定用户的活跃程度图
def showLastDays(authorname,days):
    begdate,enddate = getTimeDomain(RFF.getDateList())
    spostdate = []
    if days > 0:
        begdate = enddate - datetime.timedelta(days=days)
        spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    else:
        spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    spostdate = RFF.getPostByAuthor(authorname,spostdate)
    llen = len(spostdate)
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    if days > 30:
        ommit_xlabel_per = days/30  #忽略x label的个数
        ommit_xlabel_per-=1  #同上
        while x<=days:
            feqlist.append(0)
            timeline.append(str(xdate.month)+"-"+str(xdate.day))
            xdate += datetime.timedelta(days=1)
            feqlist[x] = getCountByDate(xdate,spostdate)
            x+=1
            ppp = 0
            while ppp < ommit_xlabel_per and x <= days:
                feqlist.append(0)
                timeline.append("")
                xdate += datetime.timedelta(days=1)
                feqlist[x] = getCountByDate(xdate,spostdate)
                x+=1
                ppp+=1
        xdate -= datetime.timedelta(days=1)
        timeline[len(timeline)-1] == str(xdate.date())
    else:
        while x < days: #初始化频率数组
            feqlist.append(0)
            timeline.append(str(xdate.month)+"-"+str(xdate.day))
            xdate += datetime.timedelta(days=1)
            feqlist[x] = getCountByDate(xdate,spostdate)
            x+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(llen)+')',timeline,feqlist,"【"+ authorname +'】的活跃程度图('+ str(begdate.date()) + "->" + str(enddate.date()) +")")
    print('>>>>>图像加载完毕')
    

#该函数用来统计满足指定日期的帖子数 *仅用于处理二级数据
#返回值：满足日期的帖子条数
def getCountByDate(date,datalist):
    #datedate = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    datedate = date
    ct = 0
    for post in datalist:
        #[[内容,时间],[...],...]
        ddate = datetime.datetime.strptime(post[2], "%Y-%m-%d %H:%M")
        if datedate.year == ddate.year and datedate.month == ddate.month and datedate.day == ddate.day:
            ct+=1
    return ct



#该函数为辅助函数，用于找出时间区间
#返回值：最早时间，最近时间
def getTimeDomain(datelist):
    datelist.sort()
    return datelist[0],datelist[len(datelist)-1]
    
#该函数用来显示指定用户的关键词
def showKeyWord(authorname,days,datalist=RFF.getPostDataList()):
    begdate,enddate = getTimeDomain(RFF.getDateList())
    spostdate = []
    if days > 0:
        begdate = enddate - datetime.timedelta(days=days)
        spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    else:
        spostdate = getPostDatebyTimeDomain(begdate,enddate,RFF.getPostDataList())
    spostdate = getPostByAuthor(authorname,spostdate)
    dp = ""
    #开始统计关键词
    #合并回帖
    for post in spostdate:
        dp += "。" + post[0]
    kd = jieba.analyse.extract_tags(dp, topK=20)
    print("\n\n贴吧ID：",authorname,":\n总共回帖长度（基于已有数据）:",len(dp),"\n关键词：\n",str(kd))

