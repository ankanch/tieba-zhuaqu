import lib.result_functions_file as RFF
import lib.maglib as MSG
import lib.graphicsData as drawGraphic
import datetime
import numpy

#KCC基本分析组件
#该组件用于统计某个词语的频率变化并以折线统计图的形式显示


#该函数用来显示过去指定天数的词频变化
def showLastDays(word,days):
    print("获取数据集中的最近时间...")
    enddate = RFF.queryDatasourceLatestTime()
    print("计算时间区间...")
    begdate = enddate - datetime.timedelta(days=days)
    print('时间区间：',begdate,'->',enddate)
    print("获取回帖列表...")
    spostdate = RFF.queryWordContainListAfterTime(str(begdate))
    print("解析回帖数据...")
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
            x+=1
            ppp = 0
            while ppp < ommit_xlabel_per and x <= days:
                feqlist.append(0)
                timeline.append("")
                xdate += datetime.timedelta(days=1)
                x+=1
                ppp+=1
        xdate -= datetime.timedelta(days=1)
        timeline[len(timeline)-1] == str(xdate.date())
    else:
        while x < days: #初始化频率数组
            feqlist.append(0)
            timeline.append(str(xdate.month)+"-"+str(xdate.day))
            xdate += datetime.timedelta(days=1)
            x+=1
    # [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
    for post in spostdate:
        if post[3].find(word) > -1:
            satpos = (post[4] - begdate).days
            feqlist[satpos-1]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,"【"+ word +'】的时间频率图('+ str(begdate.date()) + "->" + str(enddate.date()) +")")
    print('>>>>>图像加载完毕')
    

#该函数用来显示过去指定月数的词频变化
def showLastMonths(word,months):
    print("获取数据集中的最近时间...")
    enddate = RFF.queryDatasourceLatestTime()
    print("计算时间区间...")
    begdate = enddate - datetime.timedelta(days=months*30)
    print('时间区间：',begdate,'->',enddate)
    print("获取回帖列表...")
    spostdate = RFF.queryWordContainListAfterTime(str(begdate))
    print("解析回帖数据...")
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    while x < months: #初始化频率数组
        ommit_xlabel_per = months/24  #忽略x label的个数
        ommit_xlabel_per-=1  #同上
        feqlist.append(0)
        timeline.append(str(xdate.month)+"月")
        if xdate.month == 1:
            timeline[len(timeline)-1] = str(xdate.year)+"年-" + timeline[len(timeline)-1]
        xdate += datetime.timedelta(days=30)
        x+=1
        ppp = 0
        while ppp < ommit_xlabel_per and x < months:
            feqlist.append(0)
            timeline.append("")
            if xdate.month == 1:
                timeline[len(timeline)-1] = str(xdate.year)+"年-" + timeline[len(timeline)-1]
            xdate += datetime.timedelta(days=30)
            ppp+=1
            x+=1
    # [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
    for post in spostdate:
        if post[3].find(word) > -1:
            satpos = int(((post[4] - begdate).days)/30)
            feqlist[satpos-1]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,"【"+ word +'】的时间频率图(' + str(begdate.date()) + "->" + str(enddate.date()) +")")
    print('>>>>>图像加载完毕')

#该函数用来显示过去指定年的词频变化
def showLastYears(word,years):
    print("获取数据集中的最近时间...")
    enddate = RFF.queryDatasourceLatestTime()
    print("计算时间区间...")
    begdate = enddate - datetime.timedelta(days=years*365)
    print('时间区间：',begdate,'->',enddate)
    print("获取回帖列表...")
    spostdate = RFF.queryWordContainListAfterTime(str(begdate))
    print("解析回帖数据...")
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    print("begdate=",begdate,"enddate=",enddate)
    while x <= years: #初始化频率数组
        feqlist.append(0)
        timeline.append(str(xdate.year)+"年")
        print(str(xdate.year))
        xdate += datetime.timedelta(days=365)
        x+=1
    # [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
    for post in spostdate:
        if post[3].find(word) > -1:
            postdate = post[4]
            satpos = postdate.year - begdate.year
            #print("satpos=",satpos,"\tpostdate=",postdate,"\tbegdate=",begdate,"\tyear1=",postdate.year,"\tyear2=",begdate.year)
            feqlist[satpos]+=1
    #开始绘图
    drawGraphic.linePlotGraphics('时间','出现次数（帖子/回帖总数：'+str(len(spostdate))+')',timeline,feqlist,"【"+ word +'】的时间频率图('+ str(begdate.year) + "->" + str(enddate.year) +")")
    print('>>>>>图像加载完毕')




#该函数为辅助函数，用于找出时间区间
#返回值：最早时间，最近时间
    
    