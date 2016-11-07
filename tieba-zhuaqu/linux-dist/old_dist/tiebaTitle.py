#coding=utf-8
import urllib.request
import threading
import re
import os
import sys
import socket

socket.setdefaulttimeout(60)
GV_DOWNLOAD_ALL = []
GV_THEAD_COUNT = 4   #并发下载线程数
GV_FINISHED_COUNT = []
GV_MODE = 1
page = 0
x=0
max_page = 0
pocessList=[]

GV_ERROR_THREAD_DATA = []   #该变量用来储存出错线程数据，包括线程编号，当前线程下载位置，线程目标下载位置（里面储存的是list，按照该顺序排列）

def setupfiles():
    if os.path.exists('result.txt') == False:
        f = open('result.txt','w')
    if os.path.exists('result_add') == False:
        f = open('result_add','w')
    GV_FINISHED_COUNT.append(0)


def getHtml(url):
    page = urllib.request.urlopen(url,timeout=5)
    html = page.read()
    return html

def getTitle(html):
    #    <a href="/p/4745088342" title="DDD" target="_blank" class="j_th_tit ">DDDD</a>
    reg = r"<a href=\"/p/.*?class=\"j_th_tit \">.*?</a>"
    imgre = re.compile(reg)
    titlelist = re.findall(imgre,html)
    t=1
    dstr = '\r\n\t\t'
    for dta in titlelist:
        #匹配帖子标题
        k = re.sub("<a href=\"/p/.*?class=\"j_th_tit \">","",dta)
        k = re.sub("</a>","",k)
        #匹配帖子地址,用来获得作者和发帖时间
        postUrl = re.sub("<a href=\"","",dta)
        postUrl = re.sub("\" title=.*?class=\"j_th_tit \">.*?</a>","",postUrl)
        dstr = dstr + '\r\n\t\t' + k
        t+=1
    return t,dstr

#得到帖子的具体信息，包括发贴日期和发帖用户,该函数最好单独调用，否则会卡死程序
def getTieziInfo(suburl):
    html = getHtml('http://tieba.baidu.com' + suburl)
    html = html.decode('utf-8','ignore')
    #寻找时间
    head = "&quot;date&quot;:&quot;"
    tail = "&quot;,&quot;vote_crypt&quot;:&quot;&quot;,&quot;post_no&quot;"
    start = html.find(head)
    end = html.find(tail,start)
    postDate = html[start+len(head):end]
    #寻找用户名
    head = "PageData.thread = [author:\""
    tail = "\",thread_id :"
    start = html.find(head)
    end = html.find(tail,start)
    postAuthor = html[start+len(head):end]
    return postAuthor , postDate



def savetofile(data,path):
    f = open(path,'wb')
    f.write(data.encode('gb18030'))
    f.close()

def downloadPage(psum,count,begURL,beg=0):
    x=beg
    page = x*50
    GV_DOWNLOAD_ALL.append(False)
    errored = False
    while x < psum and errored == False:
        try:
            print('>>>>>Thread '+str(count)+':downloading page[',str(x + 1)+'/'+str(psum),']')
            html = getHtml(begURL + str(page))
            pocessList.append(html)
        except Exception:
            print('>>ERROR->Thread '+str(count)+':an error occoured when downloading page[',str(x + 1),'] !Script will retry later.*****DOWNLOADING ERROR.')
            GV_ERROR_THREAD_DATA.append([count,x,psum])   #返回出错页面和下载总数
            errored = True
        x += 1
        page +=50
    if errored == False:
        print('[Thread'+str(count)+']<<<<<all downloads jobs finished!')
        GV_DOWNLOAD_ALL[count-1] = True
        GV_FINISHED_COUNT[0] += 1
    else:
        #del GV_DOWNLOAD_ALL[ len( GV_DOWNLOAD_ALL ) - 1 ]
        #del GV_DOWNLOAD_ALL[ count - 1 ]
        axa = GV_ERROR_THREAD_DATA[ len( GV_ERROR_THREAD_DATA ) - 1 ]
        #print('===抛出测试:','线程编号:',axa[0],'意外终止位置:',axa[1],'目标终止位置:',axa[2])
        #input('按回车键继续...')


def pocessDataList(GV_COUNT,begURL):
    titlesum = 0
    titlelist = ''
    count = 0
    dstr = '0x0'
    m = 0
    x = 0
    NO_OUT = True
    exit_sum = 0
    while NO_OUT: 
        if( len(pocessList) > 0 ) :
            count += 1
            print('>>>>>now posscessing page [',count,'],with',titlesum,'pieces of data in all.....')
            m , dstr= getTitle(pocessList[0].decode('utf-8','ignore'))
            del pocessList[0]
            titlelist += dstr
            titlesum += m
            x = 0
            for item in GV_DOWNLOAD_ALL:
                if item == True:
                    x += 1
            #print('Pocessed finished!')
        #if x == GV_COUNT:
        if GV_FINISHED_COUNT[0] == GV_COUNT:
            NO_OUT = False
            break
            #print('1-0')
        #检测是否有线程异常，如果异常，则重新启动
        if len(GV_ERROR_THREAD_DATA) !=0:
            for item in GV_ERROR_THREAD_DATA:
                print('>>Restarting thread '+str(item[0])+'.....')
                tn = threading.Thread(target=downloadPage,args=(item[2],item[0],begURL,item[1],))
                print('>>Thread '+str(item[0])+'restart finished!')
                tn.setDaemon(True)
                tn.start()
                del GV_ERROR_THREAD_DATA[0]
    return titlesum,titlelist

