import tiebaTitle as TT
import urllib.request
import os
import sys
import time
import threading
#import dataminer
import pickle
import datetime


#该脚本用来抓取我们贴吧帖子的标题
begURL = 'http://tieba.baidu.com/f?'
#主程序逻辑
os.system('cls')
print('>>>>>该脚本用来抓取贴吧帖子的标题，可以用作舆情分析\n>>>>>by Kanch kanchisme@gmail.com')
isize = os.path.getsize('C:\\ktieba\\result.txt')
if isize > 10:
    f = open('C:\\ktieba\\result_add','rb')
    xs = pickle.load(f)
    f.close()
    print('\n\n\n>>>>>检测到数据集，是否使用现有数据集？')
    opt = input('\t>>>数据集大小：'+str(isize)+' bytes,共'+str(xs['sum'])+'条数据,创建日期：'+str(xs['time']) +'\n>>>>>是否使用？(Y/N)_____\b\b\b')
    if opt == 'Y':
        #dataminer.startPocessMoudle('C:\\ktieba\\result.txt')
        sys.exit(0)
opt = input('\r\n>>>>>是否要指定抓取的贴吧？如果不指定，将会默认抓取【成都信息工程大学】吧。（Y/N）:____\b\b')
if opt == 'Y':
    tieba_name = input('>>>>>请输入要抓取的贴吧：______________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
    print('>>>>>程序将会抓取【' + tieba_name + '】吧！')
else:
    tieba_name = '成都信息工程大学'
    print('>>>>>未指定贴吧，默认抓取【成都信息工程大学】吧！')
KWD = urllib.parse.urlencode({'kw':tieba_name})
begURL = begURL + KWD + '&ie=utf-8&pn='
TT.max_page = input('>>>>>请输入需要抓取的页数：______\b\b\b\b\b')

GTC = input('>>>>>请输入并发线程数量（程序将会使用多线程下载网页）：_____\b\b\b')
TT.GV_THEAD_COUNT = int(GTC)

mstr = "============================================================\r\n抓取结果\r\n============================================================="

#======================================================================================
#=================================主程序逻辑=======================================
#我们用一个线程下载网页，一个线程处理下载后的数据。
#======================================================================================
time1 = time.time()
TT.GV_FINISHED_COUNT.append(0)
TT.GV_TIEBANAME = tieba_name
#下面是多线程方案
MAX_PAGE = int(TT.max_page)
#创建线程
t = []   
x = 0
deltaX = MAX_PAGE / TT.GV_THEAD_COUNT
BEG = 0
END = deltaX
while x < TT.GV_THEAD_COUNT:
    tn = threading.Thread(target=TT.downloadPage,args=(int(END),x+1,begURL,int(BEG),))
    t.append(tn)
    x += 1
    BEG += deltaX
    END += deltaX


#启动线程
for item in t:
    item.setDaemon(True)
    item.start()
#循环处理数据
sum,mstr = TT.pocessDataList(TT.GV_THEAD_COUNT,begURL,tieba_name)
#===================================全部处理完毕，储存至文件======================================
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')  
last_data_source = {'sum':sum,'time':now}

f = open('C:\\ktieba\\result_add','wb')
pickle.dump(last_data_source, f,2)
f.close()
time2 = time.time()
tc = time2 - time1
print('>>>>>抓取完毕！耗时：',str(tc),'秒\n>>>>>共抓取【',sum,'】条数据\n>>>>>结果已经保存至','C:\\ktieba\\result.txt')
dd = input('>>>>>是否需要对数据进一步处理？(Y/N) ____\b\b')
if(dd == 'Y'):
    dataminer.startPocessMoudle('C:\\ktieba\\result.txt')