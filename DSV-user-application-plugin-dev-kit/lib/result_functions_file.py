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


#从数据库查询包含指定字词的所有数据集
#返回值：包含指定字词的数据集列表
def queryWordContainPostListbyKeyword(word):
    SEL = "select  CONTENT from `postdata`    where CONTENT like('%" + word +"%')"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    return datalist

#从数据库查询指定作者的所有帖子信息
#返回值：指定作者的所有回帖信息
# [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
def queryPostdataListbyAuthor(author):
    SEL = "select  * from `postdata`    where AUTHOR=\"" + author +"\""
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
def queryPostdataListAfterTime(author,earlydatestr):
    SEL = "select *   from `postdata`   where AUTHOR=\"" + author + "\" and DATE>'" + earlydatestr + "'"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    print(len(datalist))
    return datalist