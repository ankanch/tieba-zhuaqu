import tiebaTitle as TT
import urllib
import os
import sys
import time
import threading
import pickle
import datetime
import MailService

#该脚本用来抓取我们贴吧帖子的标题
begURL = 'http://tieba.baidu.com/f?'
#主程序逻辑
TT.setupfiles()
os.system('cls')
print('>>>>>This script can be used to get data from Tieba\n>>>>>by Kanch kanchisme@gmail.com')
isize = os.path.getsize('result.txt')
if isize > 10:
    f = open('result_add','rb')
    xs = pickle.load(f)
    f.close()
    print('\t>>>Dataset size:'+str(isize)+' bytes,with'+str(xs['sum'])+'pieces of data,created on'+str(xs['time']))
opt = input('\r\n>>>>>Enter the name of Tieba you\'d like to retrive?If NO,[LiYi] defaulty(Y/N):____\b\b')
if opt == 'Y':
    tieba_name = input('>>>>>Input the name of Tieba where data to retrive:______________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
    print('>>>>>Target Tieba [' + tieba_name + ']')
else:
    tieba_name = '李毅'
    print('>>>>>no specific TIeba settled,retrive data from [LiYi] defaulty')
KWD = urllib.parse.urlencode({'kw':tieba_name})
begURL = begURL + KWD + '&ie=utf-8&pn='
TT.max_page = input('>>>>>How many pages you\'d like to retrive:______\b\b\b\b\b')

GTC = input('>>>>>how many threads fit you the best:_____\b\b\b')
TT.GV_THEAD_COUNT = int(GTC)

gmode = input('>>>>>Mode Selection:1.Default 2.Deep (in Deep mode,script will get author and post data besides post title)\nEnter mode::_______\b\b\b\b')
TT.GV_MODE = int(gmode)

mstr = "============================================================\r\nRESULT\r\n============================================================="
createdtime = datetime.datetime.now()
createdtime.strftime('%Y-%m-%d %H:%M:%S')  
#======================================================================================
#=================================主程序逻辑=======================================
#我们用一个线程下载网页，一个线程处理下载后的数据。
#======================================================================================
time1 = time.time()
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
sum,mstr = TT.pocessDataList(TT.GV_THEAD_COUNT,begURL)
#===================================全部处理完毕，储存至文件======================================
now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')  
last_data_source = {'sum':sum,'time':now}

TT.savetofile(mstr,'result.txt')
f = open('result_add','wb')
pickle.dump(last_data_source, f,2)
f.close()
time2 = time.time()
tc = time2 - time1
print('>>>>>Script pocess finished!Total time cost:',str(tc),'seconds\n>>>>>with[',sum,']pieces of data in all\n>>>>>result have been save to','result.txt')


Title = "Download Success! Finised on " + str(now) + '.'
line1 = "Tieba job created on " + str(createdtime) + " now has been finised!\r\n=========================\r\nSummary\r\n\r\n"
line2 = "\r\nJob Created on: \t"+str(createdtime)+'\r\nJob finished on: \t'+str(now) +"\r\nPieces of data retrived:   " + str(sum) +"\r\nTotal time cost: \t" + str(tc) + " seconds"
line3 = "\r\n\r\n\r\n This mail is send by Kanch's PythonBot @ 216.45.55.153\r\n=========================\r\n"
Content = line1 + line2 + line3
#print(Title,'\r\n',Content)
MailService.SendMail('1075900121@qq.com',Title,Content)