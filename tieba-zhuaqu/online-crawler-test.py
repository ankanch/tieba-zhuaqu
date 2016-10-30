import tiebaTitle as TT
import urllib.request
import os
import sys
import time
import threading
import pickle
import datetime
import socket
import shareLib.TZDatagramSymbol as TZDS
import shareLib.TZautoInteractFunc as TZIF
import shareLib.TZDatagramFunc as TZDF
import shareLib.TZInternetCommunication as TZIC

#==============基本数据=======================================================

#TaskManager服务器
HOST='216.45.55.153'
PORT=50005

#贴吧BASE URL
begURL = 'http://tieba.baidu.com/f?'

#============基本数据结束======================================================

#============主程序逻辑=======================================================
#====爬虫初始化====
#主程序逻辑
TT.setupfiles()
os.system('cls')
#连接服务器
print('Tieba-zhuaqu 这是一个抓取贴吧数据的分布式爬虫\npowered by kanch \n kanchisme@gmail.com\n')
print('>>>>>启动爬虫....\n>>>>>连接TaskManager服务器中...')
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CS = True
while CS:
    try:
        s.connect((HOST,PORT))
        CS = False
    except Exception as e:
        print(e)  
print('>>>>>服务器连接成功！')
#注册爬虫
localIP = socket.gethostbyname(socket.gethostname())    #得到本地ip
LOCAL_PORT = 50006
print ("本地地址：",localIP)
data=s.recv(1024)  
print("TaskManager:\n",data.decode("utf-8"))
ID = -1
registcmd = "101," + str(localIP) + ",50006"  #向服务器发送新爬虫注册命令
s.sendall(registcmd.encode("utf-8"))  
data=s.recv(1024)  
data = data.decode("utf-8")
CID = TZDF.resolveCommand(data)[1]
CID = int(CID)   #得到分配的ID
if CID < 0 :
    print("TaskManager服务器无法完成爬虫注册：爬虫ID分配失败---->程序退出！")
    exit()
print("爬虫ID：",CID)
#====初始化完毕====================================================================
#====进入消息循环，等待任务分配======================================================
#只有当服务器传回JOB_COMFIRM (503) 状态码的时候
#才会跳出消息循环，读取任务信息。
data=s.recv(1024)
data = data.decode("utf-8")
TMCMD = int(TZDF.resolveCommand(data)[0])
print ("等待任务分配中...")
#s.sendall("700".encode("utf-8"))    #发送任务测试命令
while TMCMD != TZDS.JOB_CONFIRM:
    try:
        data=s.recv(1024)
        data = data.decode("utf-8")
        print("data=",data)
        TMCMD = int(TZDF.resolveCommand(data)[0])
        #下面的代码用于在线测试，但存在问题， 故暂时取消在线测试，直接接受任务清单，以后完善
        """if TMCMD == TZDS.ONLINE_ECHO:
            s.sendall("666,CRAWLER oNLINE - > CONFRIM".encode("utf-8"))
            data=s.recv(1024)
            data = data.decode("utf-8")
            print("data(in RMCMD=ONLINE_ECHO)=",data)
            TMCMD = int(TZDF.resolveCommand(data)[0]) 
        """
    except:
        pass
s.sendall("666,job comfirm".encode("utf-8"))
print(">>>>>接收到任务列表！")
#跳出消息循环，读取任务信息
#任务清单组成：任务代码，贴吧名字，起始抓取页码，抓取页码
#一个正确的响应为：503,李毅,10,50
#====解析并设置任务清单====
TASKDETAIL = TZDF.resolveCommand(data)
print(">>>>>抓取贴吧：",TASKDETAIL[1],",抓取第",TASKDETAIL[2],"到",TASKDETAIL[3],"页。")
KWD = urllib.parse.urlencode({'kw':TASKDETAIL[1]})
begURL = begURL + KWD + '&ie=utf-8&pn='
TT.max_page = int(TASKDETAIL[3])          #最多抓取页码
TT.GV_THEAD_COUNT = 4               #线程数量
BEGING_PAGE = int(TASKDETAIL[2])    #起始抓取页码
print(">>>>>开始抓取任务...")
#=====开始下载->>>>>=================================================================
#我们用多个线程下载网页，一个线程处理下载后的数据。
#===================================================================================
time1 = time.time()
#下面是多线程方案
MAX_PAGE = int(TT.max_page)
#创建线程
t = []   
x = 0
deltaX = MAX_PAGE / TT.GV_THEAD_COUNT
BEG = BEGING_PAGE
END = BEGING_PAGE + deltaX
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

TT.savetofile(mstr,'C:\\ktieba\\result.txt')
f = open('C:\\ktieba\\result_add','wb')
pickle.dump(last_data_source, f,2)
f.close()
time2 = time.time()
tc = time2 - time1
print('>>>>>抓取完毕！耗时：',str(tc),'秒\n>>>>>共抓取【',sum,'】条数据\n>>>>>结果已经保存至','C:\\ktieba\\result.txt')
#===================================向服务器回传任务结果======================================
FILESENDCMD = str(TZDS.JOBTRANSFER)+",Ready to send"
s.sendall(FILESENDCMD.encode("utf-8"))  
data=s.recv(1024)  
data = data.decode("utf-8")
print("TaskManager:",data)
print(">>>>>开始上传任务结果文件至TaskManager服务器...")
TZIF.sendFile(s,"C:\\ktieba\\result.txt",CID)
print(">>>>>任务进度文件上传完毕！")
print(">>>>>程序结束！")
#====发送完成消息====
FILESENDCMD = str(TZDS.FINISH)+",Ready to send"
s.sendall(FILESENDCMD.encode("utf-8"))  
data=s.recv(1024)  
data = data.decode("utf-8")
print("任务完成！爬虫初始状态，准备下次任务。")
s.sendall("102,crawler offline:job_finished".encode("utf-8"))  
os.system('python online-crawler-test.py')