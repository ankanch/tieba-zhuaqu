import csv
import pymysql
import jieba
import jieba.analyse
import os
import ast

DB_NAME = "tieba_zhuaqu"
DB_HOST = "120.77.37.235"
DB_USER =
DB_PASSWORD = 


def printb(raw):
    for x in raw:
        print("\b",end="")

#loading how schools list
def loadschools():
    print('loading school list...')
    f = open('schools.txt')
    pstr = f.read()
    f.close()
    slist = pstr.split(',')
    return slist

#loading lacation list
#returns: [ [provence,[city list] ], ]
def loadlocations():
    print('loading location list...')
    f = open('locations.txt')
    rawstr = f.read()
    f.close()
    levelone = rawstr.split('\n')
    rlt = []
    for level in levelone:
        xl = level.split('：')
        provence = xl[0]
        citylist = xl[1].split(' ')
        rlt.append([provence,citylist])
    return rlt

#determine how many jieba keyword returns depends on the length of post
def keywordcount(rawd):
    lens = len(rawd)
    if lens < 30:
        return 1
    elif lens < 58:
        return 3
    elif lens < 80:
        return 5
    elif lens < 120:
        return 7
    else:
        return 9


#application start
os.system("cls")
print("cuit tieba user analyzier\napplication start.\nconnecting to the database...")
#==
conn = pymysql.connect(host=DB_HOST, port=3306,user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME,charset='UTF8')
conn.set_charset('utf8mb4')
cur = conn.cursor()
print("database connect successfully.\ngenerating diff-user list...")
#==firstly,we have to statistics how many users are in our database
CUS = "SELECT `AUTHOR` FROM `postdata` WHERE 1"
cur.execute(CUS)
authorlist = cur.fetchall()
diffauthor = []
i=0
lenl  = "/" + str(len(authorlist))
print("\npocessing...",end="  ")
for author in authorlist:
    i+=1
    xbuf = str(i) + lenl
    print(xbuf,end="")
    if author[0] not in diffauthor:
        diffauthor.append(author[0])
    printb(xbuf)
print("diff-user list generated successfully! there are",str(len(diffauthor)),"in total.\nstart retrive keyword for each user...")
schoolslist = loadschools()
locationlist = loadlocations()
#now we have a diff-author list
#let's apply keyword retrive to each user ,then
#==strt poscess
grade = {"大一":0,"大二":0,"大三":0,"大四":0}

for author in diffauthor:
    SELPOST = "SELECT `CONTENT` FROM `postdata` WHERE `AUTHOR`=\"" + author +"\""
    print("querying <",author,"> 's post list...")
    cur.execute(SELPOST)
    conn.commit()
    postlist = cur.fetchall()
    print("retrived successfully. <",str(len(postlist)),"> pieces in total")
    print("starting analyzing...")
    pkl_jieba = []  #save every pieces of posts' keyword extarct by jieba
    for post in postlist:
        #extract keyword using jieba
        pm = jieba.analyse(post, topK=keywordcount(post), allowPOS=('ns', 'n', 'vn', 'v'))
        pkl_jieba.append(pm)
        #satistics for grade
        #satistics for location
        #satistics for schools
    #satistics every post keyword by jieba,get most 20 of them
    pkd_jieba = {}
    for jkw in pkl_jieba:
        for kw in jkw:
            if kw in pkd_jieba.keys():
                pkd_jieba[kw] += 1
            else:
                pkd_jieba[kw] = 1
    #sort all keyword and get top 20
    print(pkd_jieba.keys()[0:20]) 
    sorted(pkd_jieba.items(), key=lambda d: d[1],reverse=True)
    print(pkd_jieba.keys()[0:20]) 
    #INS = "INSERT INTO `useranalyze`( `USER`, `JIEBAKEY`, `GRADEKEY`, `SCHOOLKEY`, `LOCATIONKEY`, `RESERVE`) VALUES ()"

#cur.execute(SEL)

#==pocess finished
print("application completed pocessing.\nclosing session...")
#conn.commit()
cur.close()
conn.close()
print("application exit.")


