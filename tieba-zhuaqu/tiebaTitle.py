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
    if os.path.exists('C:\\ktieba') == False:
        os.makedirs( "C:\\ktieba" )
    if os.path.exists('C:\\ktieba\\result.txt') == False:
        f = open('C:\\ktieba\\result.txt','w')
    if os.path.exists('C:\\ktieba\\result_add') == False:
        f = open('C:\\ktieba\\result_add','w')
    if os.path.exists('C:\\ktieba\\ignoreWords') == False:
        f = open('C:\\ktieba\\ignoreWords','w')
    GV_FINISHED_COUNT.append(0)


def getHtml(url):
    try:
        page = urllib.request.urlopen(url,timeout=5)
        html = page.read()
        return html
    except Exception as e:
        print("->读取出错")
        return ""

def getTitle(html):
    #    <a href="/p/4745088342" title="DDD" target="_blank" class="j_th_tit ">DDDD</a>
    reg = r"<a href=\"/p/.*?class=\"j_th_tit \">.*?</a>"
    imgre = re.compile(reg)
    titlelist = re.findall(imgre,html)
    t=1
    sum = len(titlelist)
    dstr = '\r\n\t\t'
    author = ""
    date = ""
    replydata = ""
    for dta in titlelist:
        #匹配帖子标题
        #print(t,'/',sum,"",end=" ")
        print("#",end="")
        sys.stdout.flush()
        k = re.sub("<a href=\"/p/.*?class=\"j_th_tit \">","",dta)
        k = re.sub("</a>","",k)
        #匹配帖子地址,用来获得作者和发帖时间
        postUrl = re.sub("<a href=\"","",dta)
        postUrl = re.sub("\" title=.*?class=\"j_th_tit \">.*?</a>","",postUrl)
        author , date , replydata = getTieziInfo(postUrl)
        dstr = dstr + '\r\n\t\t' + k + "@#@" + author + "@#@" + date + "@#@" + replydata
        t+=1
    print("\n")
    GV_FINISHED_COUNT[0] += 1
    return t,dstr

#得到帖子的具体信息，包括发贴日期和发帖用户以及第一页里面的回帖,该函数最好单独调用，否则会卡死程序
def getTieziInfo(suburl):
    html = getHtml('http://tieba.baidu.com' + suburl)
    html = html.decode('utf-8','ignore')
    #寻找用户名
    head = "PageData.thread = {author:\""
    tail = "\",thread_id :"
    start = html.find(head)
    end = html.find(tail,start)
    postAuthor = html[start+len(head):end]
    #寻找回帖
    start = html.find(head)
    end = html.find(tail,start)
    reply = html[start+len(head):end]
    html = html[end+len(tail):]
    reply = onlyCHS(reply)
    #寻找时间
    head = "&quot;date&quot;:&quot;"
    tail = "&quot;,&quot;vote_crypt&quot;:&quot;&quot;,&quot;post_no&quot;"
    start = html.find(head)
    end = html.find(tail,start)
    postDate = html[start+len(head):end]
    html = html[end+len(tail):]

    replydata = ""
    #print("NOT IN WHILE:postAuthor=",postAuthor,"\tpostDate=",postDate,"\treply=",reply)
    replydata = replydata + reply + "*#*" + postAuthor + "*#*" + postDate +"$#$"
    #上面的代码完成了1楼信息的抓取
    #接下来寻找第一页的回帖内容================================
    #寻找该页的所有回帖内容
    head = " j_d_post_content  clearfix\">            "
    tail = "</div><br></cc><br><div class=\"user-hide-post-down\" style=\"display: none;\"></div>"
    #寻找发帖用户
    username_head="<img username=\""
    username_tail="\" class=\"\" src=\""
    #寻找发帖时间
    postdate_head="&quot;date&quot;:&quot;"
    postdate_tail="&quot;,&quot;vote_crypt&quot;:&quot;&quot;,&quot;post_no&quot;"
    while True:
        if html.find(tail) < 0:
            break
        #寻找作者
        start = html.find(username_head)
        end = html.find(username_tail)
        author = html[start+len(username_head):end]
        html = html[end+len(username_tail):]
        #print("author=",author,"\tstart=",start,"\tend=",end)
        #寻找回帖内容
        start = html.find(head)
        end = html.find(tail,start)
        reply = html[start+len(head):end]
        html = html[end+len(tail):]
        reply = onlyCHS(reply)
        #print("reply=",reply)
        #找到了一个回复，接下来寻找作者和发帖时间
        #寻找发帖时间
        start = html.find(postdate_head)
        end = html.find(postdate_tail)
        date = html[start+len(postdate_head):end]
        html = html[end+len(postdate_tail):]
        #print("post date=",date,"\tstart=",start,"\tend=",end)
        
        #os.system("pause")
        replydata = replydata + reply + "*#*" + author + "*#*" + date +"$#$"
    #返回结果
    return postAuthor , postDate , replydata

#该函数用来去掉回帖中无关HTML标签，只保留中文/英文
def onlyCHS(reply):
    #回复里面的多于图片标签
    ex_img_head = "<img"
    ex_img_tail = ">"
    ex_div_head = "<div"
    ex_div_tail = ">"
    ex_a_head = "<a href="
    ex_a_tail = "</a>"
    #去掉贴吧表情之类的内嵌HTML标签
    imgstart = reply.find(ex_img_head)
    reply = reply.replace("<br>","")
    #清除img
    while True:
        #print("imgstart=",imgstart,"reply=",reply)
        #os.system("pause")
        if imgstart < 0 or reply.find(ex_img_tail) < 0:
            break
        reply = reply[:imgstart] + reply[reply.find(ex_img_tail,imgstart)+len(ex_img_tail):]
        imgstart = reply.find(ex_img_head)
        #print("\timg-clear-while:\treply=",reply)
    #清除div
    divstart = reply.find(ex_div_head)
    reply = reply.replace("</div>","")
    while True:
        #print("divstart=",imgstart,"reply=",reply)
        #os.system("pause")
        if divstart < 0 or reply.find(ex_div_tail) < 0:
            break
        reply = reply[:divstart] + reply[reply.find(ex_div_tail,divstart)+len(ex_div_tail):]
        divstart = reply.find(ex_div_head)
        #print("\tdiv-clear-while:\treply=",reply)    
     #清除a
    astart = reply.find(ex_a_head)
    while True:
        #print("astart=",imgstart,"reply=",reply)
        #os.system("pause")
        if astart < 0 or reply.find(ex_a_tail) < 0:
            break
        reply = reply[:astart] + reply[reply.find(ex_a_tail,astart)+len(ex_a_tail):]
        astart = reply.find(ex_a_head)
        #print("\tdiv-clear-while:\treply=",reply)
    return reply    


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
            print('>>>>>线程 '+str(count)+'：当前正在下载第【',str(x + 1)+'/'+str(psum),'】页数据')
            html = getHtml(begURL + str(page))
            pocessList.append(html)
        except Exception:
            print('>>错误->线程 '+str(count)+'：在下载第【',str(x + 1)+'/'+str(psum),'】页数据时出错！程序将会重试。*****下载出错。')
            GV_ERROR_THREAD_DATA.append([count,x,psum])   #返回出错页面和下载总数
            errored = True
        x += 1
        page +=50
    if errored == False:
        print('【线程'+str(count)+'】<<<<<页面全部下载完成！')
        GV_DOWNLOAD_ALL[count-1] = True
        #GV_FINISHED_COUNT[0] += 1
    else:
        axa = GV_ERROR_THREAD_DATA[ len( GV_ERROR_THREAD_DATA ) - 1 ]


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
            print('>>>>>当前正在处理第【',count,'】页数据,已抓取',titlesum,'条数据.....',end=' ')
            m , dstr= getTitle(pocessList[0].decode('utf-8','ignore'))
            del pocessList[0]
            titlelist += dstr
            titlesum += m
            x = 0
            for item in GV_DOWNLOAD_ALL:
                if item == True:
                    x += 1
            print('子线程处理完毕！','调试：x=',x,'GV_COUNT=',GV_COUNT)
        if GV_FINISHED_COUNT[0] == GV_COUNT:
            NO_OUT = False
            break
        #检测是否有线程异常，如果异常，则重新启动
        if len(GV_ERROR_THREAD_DATA) !=0:
            for item in GV_ERROR_THREAD_DATA:
                print('>>尝试重新启动线程 '+str(item[0])+'中.....')
                tn = threading.Thread(target=downloadPage,args=(item[2],item[0],begURL,item[1],))
                print('>>线程 '+str(item[0])+'重新启动完成！')
                tn.setDaemon(True)
                tn.start()
                del GV_ERROR_THREAD_DATA[0]
    return titlesum,titlelist

