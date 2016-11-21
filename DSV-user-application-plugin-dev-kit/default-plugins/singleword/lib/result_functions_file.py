import os
import datetime
import lib.maglib as MSG
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

DBCONN = None
DBCUR = None


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
        #print(DBSETTINGS[db[0]])
    return data
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

