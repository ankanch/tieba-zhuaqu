import os
import datetime
import lib.maglib as MSG
#这是一个对结果进行初步处理的库
#用来分离抓取结果，作者，发帖时间
#抓取结果应该储存在【用户端根目录】并以result命名
#在测试情况下，抓取结果文件为results.txt
#重要全局变量
PATH_SUFFIX = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
PATH_SUFFIX = PATH_SUFFIX[:len(PATH_SUFFIX)-8]
PATH_RESULT_FILE =  PATH_SUFFIX + "\\result.txt"

#该函数返回帖子列表，进行第一步分离，用于分离帖子基本信息和回帖信息
#返回格式：2个元素的list v 
# [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
def getPostDataList():
    rawresult = openResult()
    rawpost = spiltRawPost(rawresult)
    SPILT_TITLE_PDATA = "@#@"
    SPILT_INNER_DATA = "*#*"
    SPILT_INNER_REPLY = "$#$"
    postdata = []
    for post in rawpost:
        if len(post) < 9:
            continue
        spd = post.split(SPILT_TITLE_PDATA) #spd[0]=标题数据 spd[1]=回帖数据
        titledata = spd[0].split(SPILT_INNER_DATA)
        try:
            replylist = spd[1].split(SPILT_INNER_REPLY)
            replydata = []
            for reply in replylist:
                rep = reply.split(SPILT_INNER_DATA)
                replydata.append(rep)
            postdata.append([titledata,replydata])
        except:
            print("replydata error,no index 2")
    return postdata

#该函数的作用是返回贴吧标题与回帖列表
#返回格式：类型为字符串的list
def getContentList():
    postdata = getPostDataList()
    contentlist = []
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in postdata:
        contentlist.append(post[0][0])
        replylist = post[1]
        for reply in replylist:
            contentlist.append(reply[0])
    return contentlist

#该函数的作用是返回所有发帖日期的集合
#返回格式：被分割的时间list 
# [[年,月,日,小时,分钟],[.....],.....] (int)
def getDateList():
    postdata = getPostDataList()
    datelist = []
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in postdata:
        datelist.append(datetime.datetime.strptime(post[0][2], "%Y-%m-%d %H:%M"))
        replylist = post[1]
        for reply in replylist:
            if len(reply) < 3:
                continue
            datelist.append(datetime.datetime.strptime(reply[2], "%Y-%m-%d %H:%M"))
    return datelist


#该函数的作用是返回所有作者集合
#返回格式：类型为字符串的list 
def getAuthorList():
    postdata = getPostDataList()
    authorlist = []
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in postdata:
        authorlist.append(post[0][1])
        replylist = post[1]
        for reply in replylist:
            authorlist.append(reply[1])
    return authorlist

#该函数用于统计各个词语的出现次数
#函数返回：一个任意字符串和指定词语的出现次数
def satisticWord(word,datalist):
    os.system('cls')
    print('>>>>>开始统计【',word,'】出现次数....')
    sum=1
    mlist=[]
    for item in datalist:
        if item.find(word) != -1:
            sum+=1
            mlist.append(item)
        print('>',end='')
    print('>>>>>统计完成！\n\n')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',len(datalist),'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    for item in mlist:
        print('\t◆\t',item)
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',len(datalist),'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    return 'SW',sum-1

#=======================本文件内的辅助函数<主要用于文件操作>==========================

#打开抓取结果文件
#函数返回：文件内容
def openResult():
    print("任务结果文件：",PATH_RESULT_FILE)
    f = open(PATH_RESULT_FILE,'rb')
    data = f.read()
    f.close()
    data = data.decode('gbk', 'ignore')
    return data

#将openResult()读取出来的数据按行分开,因为一行就是一个post
#函数返回：list -> 每一行的数据
def spiltRawPost(rawdata):
    datalist = rawdata.split('\r\n\t\t')
    return datalist


#postdata = getPostDataList()
#print("len(postdata)=",len(postdata),"\tlen(postdata[0])=",len(postdata[0]),"\tlen(postdata[1])=",len(postdata[1]))
#print(str(postdata))