import lib.result_functions_file as RFF
import lib.maglib as MSG
import lib.graphicsData as drawGraphic
import datetime
import numpy

#这个库是用来统计某个词语的频率变化并以折线统计图的形式显示
#这是tieba-zhuaqu项目的用户端基本插件
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
        #timeline.append(str(xdate.date().month)+"."+str(xdate.date().day))
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


#该函数用于从外部执行
def extrenSingleWordTF():
    word = input("请输入要统计的词语：")
    singleWordTF(word,RFF.getPostDataList(),scale=30)

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