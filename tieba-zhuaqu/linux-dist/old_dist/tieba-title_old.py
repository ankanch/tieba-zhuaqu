#coding=utf-8
import urllib.request
import re
import os
import sys
import threading
import datetime
import pickle
import time
import MailService


begURL = 'http://tieba.baidu.com/f?'
PATH_DOWNLOAD_CACHE = sys.path[0]+'\\dlcache\\'   
GV_DOWNLOAD_ALL = []
GV_THEAD_COUNT = 4
page = 0
x=0
max_page = 0
sum = 0
pocessList=[]

def setupfiles():
    if os.path.exists('result.txt') == False:
        f = open('result.txt','w')
    if os.path.exists('result_add') == False:
        f = open('result_add','w')

def getHtml(url):
    page = urllib.request.urlopen(url)
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
        k = re.sub("<a href=\"/p/.*?class=\"j_th_tit \">","",dta)
        k = re.sub("</a>","",k)
        #print('\t',k.encode('utf-8'))
        dstr = dstr + '\r\n\t\t' + k
        t+=1
    return t,dstr

def savetofile(data,path):
    f = open(path,'wb')
    f.write(data.encode('gb18030'))
    f.close()

def downloadPage(psum,count,beg=0):
    x=beg
    page = x*50
    GV_DOWNLOAD_ALL.append(False)
    while x < psum:
        #os.system('cls')
        print('>>>>>thead '+str(count)+':now downloading page[',str(x + 1)+'/'+str(psum),']')
        html = getHtml(begURL + str(page))
        pocessList.append(html)
        x += 1
        page +=50
    print('[thead'+str(count)+']<<<<<All pages downloaded!')
    GV_DOWNLOAD_ALL[count-1] = True


def pocessDataList(GV_COUNT):
    titlesum = 0
    titlelist = ''
    count = 0
    dstr = '0x0'
    m = 0
    NO_OUT = True
    while NO_OUT: 
        if( len(pocessList) > 0 ):
            count += 1
            print('>>>>>now pocess page[',count,'],------[',titlesum,']pieces of data in all')
            m , dstr= getTitle(pocessList[0].decode('utf-8','ignore'))
            del pocessList[0]
            titlelist += dstr
            titlesum += m
            x = 0
            for item in GV_DOWNLOAD_ALL:
                if item == True:
                    x += 1
            if x == GV_COUNT:
                NO_OUT = False
                break
    return titlesum,titlelist

setupfiles()
os.system('clear')
print('>>>>>    This script used to download data from Tieba\n>>>>>by Kanch kanchisme@gmail.com')
isize = os.path.getsize('result.txt')
if isize > 10:
    f = open('result_add','rb')
    xs = pickle.load(f)
    f.close()
    print('>>>>>data dectecrd\n\t>>>size:'+str(isize)+' bytes,with '+str(xs['sum'])+' pieeces of data,created on:'+str(xs['time']) +'\n')
opt = input('\r\n>>>>>Would you like to set the Tieba with script going to collect?(if not,script will collect CUIT ba)(Y/N):____\b\b')
if opt == 'Y':
    tieba_name = input('>>>>>please enter the name you wish to collect:______________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
    print('>>>>>script will collect [SET NO SHOW ]!')
else:
    tieba_name = '成都信息工程大学'
    print('>>>>>no settleed Tieba,collect CUIT defaultly')
KWD = urllib.parse.urlencode({'kw':tieba_name})
begURL = begURL + KWD + '&ie=utf-8&pn='
max_page = input('>>>>>how many page you wish to collect?:______\b\b\b\b\b')
TC = input('how many theads you\'d like to run?____\b\b\b')
GV_THEAD_COUNT = int(TC)

mstr = "============================================================\r\nRESULT\r\n============================================================="

createdtime = datetime.datetime.now()
createdtime.strftime('%Y-%m-%d %H:%M:%S')  

time1 = time.time()
#下面是多线程方案
MAX_PAGE = int(max_page)
#创建线程
t = []   
x = 0
deltaX = MAX_PAGE / GV_THEAD_COUNT
BEG = 0
END = deltaX
while x < GV_THEAD_COUNT:
    tn = threading.Thread(target=downloadPage,args=(int(END),x+1,int(BEG),))
    t.append(tn)
    x += 1
    BEG += deltaX
    END += deltaX

for item in t:
    item.setDaemon(True)
    item.start()
#循环处理数据
sum,mstr = pocessDataList(GV_THEAD_COUNT)
#===================================全部处理完毕，储存至文件======================================
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')  
last_data_source = {'sum':sum,'time':now}

savetofile(mstr,'result.txt')
f = open('result_add','wb')
pickle.dump(last_data_source, f,2)
f.close()
time2 = time.time()
tc = time2 - time1
print('>>>>>Collect Success,total time cost:',str(tc),'sec\n>>>>>total data collect[',sum,']\n>>>>>result save to ','result.txt')

Title = "Download Success! Finised on " + str(now) + '.'
line1 = "Tieba job created on " + str(createdtime) + " now has been finised!\r\n=========================\r\nSummary\r\n\r\n"
line2 = "\r\nJob Created on: \t"+str(createdtime)+'\r\nJob finished on: \t'+str(now) +"\r\nPieces of data retrived:   " + str(sum) +"\r\nTotal time cost: \t" + str(tc) + " seconds"
line3 = "\r\n\r\n\r\n This mail is send by Kanch's PythonBot @ 216.45.55.153\r\n=========================\r\n"
Content = line1 + line2 + line3
#print(Title,'\r\n',Content)
MailService.SendMail('james0121@vip.qq.com',Title,Content)