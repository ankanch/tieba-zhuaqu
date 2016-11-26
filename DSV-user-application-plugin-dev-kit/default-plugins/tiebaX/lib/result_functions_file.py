import os
import datetime
import lib.maglib as MSG
import pymysql
#这是一个对结果进行初步处理的库
#用来分离抓取结果，作者，发帖时间
#抓取结果应该储存在【用户端根目录】并以result命名
#在测试情况下，抓取结果文件为results.txt
#重要全局变量
PATH_SUFFIX = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
print(PATH_SUFFIX)
PATH_SUFFIX = PATH_SUFFIX[::-1]
PATH_SUFFIX = PATH_SUFFIX[PATH_SUFFIX.find('\\'):]
PATH_SUFFIX = PATH_SUFFIX[::-1]
print(PATH_SUFFIX)
PATH_RESULT_FILE =  PATH_SUFFIX + "\\datasource.ini"

DBSETTINGS = {'H':'', #HOST
              'U':'', #USER
              'P':'', #PASSWORD
              'D':''} #DATABASE_NAME

#该函数用于读取数据源信息
#返回值：成功true，否则false
def loadDataSource():
    print("加载数据源配置：",PATH_RESULT_FILE)
    f = open(PATH_RESULT_FILE,'rb')
    data = f.read()
    f.close()
    data = data.decode('gbk', 'ignore')
    dbl = data.split("\r\n")
    for db in dbl:
        DBSETTINGS[db[0]] = db[db.find('=')+1:].replace('\'','').replace(' ','')
    return data

loadDataSource()
DBCONN = pymysql.connect(host=DBSETTINGS['H'], port=3306,user=DBSETTINGS['U'],passwd=DBSETTINGS['P'],db=DBSETTINGS['D'],charset='UTF8')
DBCUR = DBCONN.cursor()


#该函数的作用是返回所有发帖日期的集合
#返回格式：被分割的时间list 
# [[年,月,日,小时,分钟],[.....],.....] (int)
def getDateList(rawdata):
    postdata = getPostDataList(rawdata)
    datelist = []
    # [ [[帖子标题,作者,发帖时间] , [回帖列表：[回帖内容,作者,回帖时间],[回帖内容,作者,回帖时间],[[......]],.....]] ]
    for post in postdata:
        datelist.append(datetime.datetime.strptime(post[0][2], "%Y-%m-%d %H:%M"))
        replylist = post[1]
        for reply in replylist:
            if len(reply) < 3:
                continue
            try:
                datelist.append(datetime.datetime.strptime(reply[2], "%Y-%m-%d %H:%M"))
            except Exception as e:
                print("x",end="")
    del postdata
    return datelist


#该函数用于统计各个词语的出现次数
#函数返回：一个任意字符串和指定词语的出现次数
def satisticWord(word):
    os.system('cls')
    print('>>>>>开始统计【',word,'】出现次数....')
    sum=1
    mlist=[]
    mlist = RFF.queryWordContainList(word)
    sum = len(mlist)
    print('>>>>>统计完成！\n\n')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',0,'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    for item in mlist:
        try:
            print('\t◆\t',item[0])
        except Exception as e:
            print('\t◆\t<<无法编码字符>>')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',0,'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    return 'SW',sum-1

#=======================本文件内的辅助函数<主要用于文件操作>==========================

#从数据库查询包含指定字词的所有数据集
#返回值：包含指定字词的数据集列表
def queryWordContainListbyKeyword(word):
    SEL = "select  CONTENT from `postdata`    where CONTENT like('%" + word +"%')"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist

#从数据库查询指定作者的所有帖子信息
#返回值：指定作者的所有回帖信息
# [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
def queryWordContainListbyAuthor(author):
    SEL = "select  * from `postdata`    where AUTHOR=\"" + author +"\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist

#从数据库查询回复给指定用户的所有其它用户列表
#返回值：用户列表 
# [ "1","2",....]
def queryUserListbyReplyto(author):
    SEL = "select  AUTHOR from `postdata`    where REPLYTO=\"" + author +"\" and AUTHOR!=\"" + author + "\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist

#从数据库查询指定用户回复给指定用户的帖子列表
#返回值：贴子列表
# [ "1","2",....]
def queryContentListbyAuthorToReplyto(fromauthor,toauthor):
    SEL = "select  CONTENT from `postdata`    where REPLYTO=\"" + toauthor +"\" and AUTHOR!=\"" + fromauthor + "\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist

#从数据库查询最大日期
#返回值：一个最大日期
def queryDatasourceLatestTime():
    SEL = "select MAX(DATE) from `postdata`"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist[0][0]

#从数据库查询小日期
#返回值：一个最小日期
def queryDatasourceEarlyTime():
    SEL = "select MIN(DATE) from `postdata`"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist[0][0]

#从数据库查询指定作者的指定日期之间的数据集
#返回值：指定日期之间的数据集列表
# [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
def queryContainListAfterTime(author,earlydatestr):
    SEL = "select *   from `postdata`   where AUTHOR=\"" + author + "\" and DATE>'" + earlydatestr + "'"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    print(len(datalist))
    return datalist

def queryAllAuthorList(tiebaname):
    SEL = "select AUTHOR   from `postdata`   where TIEBANAME=\"" + tiebaname + "\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    print(len(datalist))
    return datalist

