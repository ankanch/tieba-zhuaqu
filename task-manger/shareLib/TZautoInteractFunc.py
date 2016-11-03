#coding=utf-8
import datetime
import os
import time
import shareLib.TZDatagramSymbol as TZDS
import shareLib.TZDatagramFunc as TZDF   
import shareLib.TZInternetCommunication as TZIC

#对应的状态响应函数
#该函数用于自动化响应请求
#传入参数：命令，socket对象，爬虫计数id，已注册爬虫列表
def autoInteract(relcmd,conn,crawlerid,crawlerlist):
    cmd = 123
    cmd_head = int(relcmd[0])
    print("cmd_head=",cmd_head)
    CRLCHANGE = False
    CRLCHANGE_LIST = []
    if cmd_head == TZDS.FINISH:    #完成交互，暂时断线
        cmd = TZDF.makeUpCommand(TZDS.OKCLOSE,["crawler has been temparily disconnect to the server"])
    elif cmd_head == TZDS.REGISTE:  #将爬虫注册至服务器
        crawlerlist.append([str(crawlerid),str(relcmd[1]),int(relcmd[2]),conn])
        setDate(TZDS.DATA_CRAWLER_LIST,crawlerlist)
        cmd = TZDF.makeUpCommand(TZDS.ONLINE_ECHO,[crawlerid,"crawler has been registe to server"])
        TZIC.clientInterreactiveSend(conn,cmd)
    elif cmd_head == TZDS.JOBSTATUS:    #从爬虫那里获取完成进度  CODE,ID,POCESS RATE
        pstatus = str(relcmd[2])
        setDate(TZDS.DATA_CRAWLER_STATUS,pstatus,crawlerid=crawlerid)
        showMsg("recive pocess rate:" + str(pstatus),crawlerid)
        cmd = TZDF.makeUpCommand(TZDS.OK,["crawler job status recived"])
    elif cmd_head == TZDS.JOBTRANSFER:  #上传爬取结果文件至服务器
        cmd = TZDF.makeUpCommand(TZDS.OK,["ready to transfer"])
        TZIC.clientInterreactiveSend(conn,cmd)
        recvFile(conn,crawlerid=crawlerid)
    elif cmd_head == TZDS.ADMIN_STATUS: #回传总体处理率到管理端
        Updata()
        sum = getData(TZDS.DATA_TOTAL_AVERAGE_STATUS)
        cmd = TZDF.makeUpCommand(TZDS.OK,[str(sum),"server total task status sended"])
    elif cmd_head == TZDS.ADMIN_CRAWLER_LIST:   #从服务器端获取在线爬虫列表
        strIDList = []
        for item in crawlerlist:
            strIDList.append( [item[0],item[1],item[2]] )
        strIDList = str(strIDList)
        strIDList = strIDList.replace(",","@")
        strIDList = strIDList.replace("[","")
        strIDList = strIDList.replace("]","")
        strIDList = strIDList.replace("'","")
        strIDList = strIDList.replace(" ","")
        print("\t\t\t",strIDList)
        cmd = TZDF.makeUpCommand(TZDS.CRAWLER_LIST,[strIDList,"crawler list has been sended"])
    elif cmd_head == TZDS.ADMIN_JOBCREATE:  #接收管理端创建的任务 CODE,ADMINID,TIEBANAME,PAGE
        if str(relcmd[1]) == TZDS.ESSEN_ADMIN_CODE:
            TiebaName = str(relcmd[2])
            Pages = int(relcmd[3])
            setDate(TZDS.DATA_POCESS_TIEBA_NAME,TiebaName)
            setDate(TZDS.DATA_POCESS_PAGES_TO,Pages)
            rr = "TiebaName=" + TiebaName +";pages to pocess=" + str(Pages)
            print("\t\t\twaiting for Admin confirm job...")
            cmd = TZDF.makeUpCommand(TZDS.JOB_CONFIRM,[rr,"confirm job ?"])
            TZIC.clientInterreactiveSend(conn,cmd)
            got,data = TZDF.getPerferResponse(TZDS.OK,conn)   #perfer: OK
            if got == True:
                #先假设所有爬虫都是在线的
                onlinecount = len(crawlerlist)
                 #一次爬虫在线验证
                clist = crawlerlist
                onlineclist = []
                i = 0
                sum = len(clist)
                for crawler in clist:
                    i+=1
                    print("\t\t\tchecking online  for #",i," / ",sum," crawler...",end="\t")
                    cmd = TZDF.makeUpCommand(TZDS.OK,["tiebaname,aledpages,","aledpages + avpages"])
                    try:
                        crawler[3].sendall(cmd.encode("utf-8"))
                        onlineclist.append(crawler)
                        print("\tOK")
                    except Exception as e:
                        print("\tFAILED")
                        onlinecount-=1
                        CRLCHANGE = True
                #开始正式分配任务
                setDate(TZDS.DATA_CRAWLER_LIST,onlineclist)
                CRLCHANGE_LIST = onlineclist
                print("\t\t\tJob Confirmed by Admin.")
                avergepage = int(Pages / onlinecount)
                print("\t\tallocate job...")
                allocateJobs(TiebaName,avergepage,onlinecount,onlineclist)
                print("\t\t\tjob allocate done!")
            else:
                cmd = TZDF.makeUpCommand(TZDS.OKCLOSE,["Job allocate interrupt by admin"])
        else:
            cmd = TZDF.makeUpCommand(TZDS.ERROR,["ADMIN IDENTIFY FAILED!"])
    elif cmd_head == TZDS.ADMIN_JOBTRANSFER:    #传送所有抓取结果至admin端
        gatherSubjobs()
        sendFile(conn,"/../tieba-zhuaqu/reciveCache/tresult.txt")
        cmd = TZDF.makeUpCommand(TZDS.START_TRANSFER,["transfer done"])
    elif cmd_head == TZDS.ADMIN_SHUTDOWN:   #关闭任务管理服务器
        cmd = TZDF.makeUpCommand(TZDS.OKCLOSE,["task server is going offline"])
    elif cmd_head == TZDS.ONLINE_ECHO:  #线路联通测试
        cmd = TZDF.makeUpCommand(TZDS.ONLINE_ECHO,[" online - connection is ok"])
    elif cmd_head == TZDS.ADMIN_ONLINE:  #
        cmd = TZDF.makeUpCommand(TZDS.ONLINE_ECHO,[" Admin is online"])
    elif cmd_head == TZDS.FACTORY_TEST:
            cmd = TZDF.makeUpCommand(TZDS.JOB_CONFIRM,["成都信息工程大学","0","8"])
            print("--TEST MODE---")
    #print("\t\t\tautoInteract() return with cmd:",cmd)
    return cmd,CRLCHANGE,CRLCHANGE_LIST


#对应状态下响应下的函数定义
#消息显示函数
def showMsg(msg,crawlerid=0):
    print("\t\t\tcrawler#",str(crawlerid),":",msg)

#文件接收
def recvFile(conn,crawlerid=0):
    if(os.path.exists("/../tieba-zhuaqu/reciveCache") == False):
        os.mkdir("/../tieba-zhuaqu/reciveCache")
    filename = "/../tieba-zhuaqu/reciveCache/subjob" + str(crawlerid)
    filesize = TZIC.clientInterreactiveRecv(conn)
    showMsg(filesize)
    filesize = int(filesize)
    showMsg("filesize to recive=" + str(filesize),crawlerid=crawlerid)
    f = open(filename,'wb')
    showMsg("stat receiving...",crawlerid=crawlerid)
    recvd_size = 0
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            rdata = TZIC.clientInterreactiveRecvNOENCODE(conn,size=1024)
            recvd_size += len(rdata)
        else:
            rdata = TZIC.clientInterreactiveRecvNOENCODE(conn,size=filesize - recvd_size) 
            recvd_size = filesize
        f.write(rdata)
    f.close()
    showMsg("receive done",crawlerid=crawlerid)

def recvFileAdmin(conn,crawlerid=0):
    if(os.path.exists("../reciveCache") == False):
        os.mkdir("../reciveCache")
    filename = "../reciveCache/tresult.txt" + str(crawlerid)
    filesize = TZIC.clientInterreactiveRecv(conn)
    showMsg(filesize)
    filesize = int(filesize)
    showMsg("filesize to recive=" + str(filesize),crawlerid=crawlerid)
    f = open(filename,'wb')
    showMsg("stat receiving...",crawlerid=crawlerid)
    recvd_size = 0
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            rdata = TZIC.clientInterreactiveRecvNOENCODE(conn,size=1024)
            recvd_size += len(rdata)
        else:
            rdata = TZIC.clientInterreactiveRecvNOENCODE(conn,size=filesize - recvd_size) 
            recvd_size = filesize
        f.write(rdata)
    f.close()
    showMsg("receive done",crawlerid=crawlerid)

#文件发送
def sendFile(conn,filename="result.txt",crawlerid=0):
    filepath = filename
    showMsg("ready to send file...",crawlerid=crawlerid)
    filesize = str(os.path.getsize(filepath))
    TZIC.clientInterreactiveSend(conn,filesize) 
    showMsg("filesize:" + str(filesize),crawlerid=crawlerid)
    time.sleep(5)
    f = open(filepath,'rb')
    showMsg("start sending file",crawlerid=crawlerid)
    while True:
        filedata = f.read(1024)
        if not filedata:
            break
        TZIC.clientInterreactiveSendNOCODE(conn,filedata)
    f.close()
    showMsg("file sent completed!",crawlerid=crawlerid)


#用于数据交换
dataPackage = {}
#初始化数据交互变量
def InitDataExchangeTZautoInteractFunc():
    dataPackage[TZDS.DATA_CRAWLER_STATUS] = {}
    dataPackage[TZDS.DATA_TOTAL_AVERAGE_STATUS] = 0.0
    #dataPackage[TZDS.DATA_CRAWLER_LIST] = []
#外部数据交换函数：增加储存数据
def setDate(strname,data,crawlerid=-1):
    if strname == TZDS.DATA_CRAWLER_STATUS:
        dataPackage[TZDS.DATA_CRAWLER_STATUS][crawlerid] = data
    else:
        dataPackage[strname] = data
#外部数据交换函数：获得储存数据
def getData(strname,crawlerid=-1):
    if strname == TZDS.DATA_CRAWLER_STATUS:
        return dataPackage[TZDS.DATA_CRAWLER_STATUS][crawlerid]
    else:
        try:
            return dataPackage[strname]
        except Exception:
            print("ERROR:",strname,"no attribute!")
            return []

def delData(strname,crawlerid):
    if strname == TZDS.DATA_CRAWLER_STATUS:
        del dataPackage[TZDS.DATA_CRAWLER_STATUS][crawlerid]
    else:
        del dataPackage[strname]

#数据更新函数
def Updata():
    #更新总处理率
    sum = 0.0
    ct = 0
    for item in dataPackage[TZDS.DATA_CRAWLER_STATUS]:
        sum = sum + float(dataPackage[TZDS.DATA_CRAWLER_STATUS][item])
        ct+=1
    sum = sum / ct
    setDate(TZDS.DATA_TOTAL_AVERAGE_STATUS,sum)


#向每个爬虫分配任务
def allocateJobs(tiebaname,avpages,onlinecount,clist):
    sum = int(avpages*onlinecount)
    clist# = getData(TZDS.DATA_CRAWLER_LIST)
    aledpages = 0
    i=0
    sum = len(clist)
    for crawler in clist:
        i+=1
        print("\t\t\tAllocating for #",i," / ",sum," crawler...")
        cmd = TZDF.makeUpCommand(TZDS.JOB_CONFIRM,[tiebaname,aledpages,aledpages + avpages])
        aledpages+=avpages
        crawler[3].sendall(cmd.encode("utf-8"))
    print("TZ TaskManager: Jobs has been allocate to ",onlinecount,"crawlers")


#将所有子任务文件合成一个文件
def gatherSubjobs():
    flist = os.listdir("/../tieba-zhuaqu/reciveCache")
    tgfile = open("/../tieba-zhuaqu/reciveCache/tresult.txt","w")
    tgfile.truncate()
    tgfile.close()
    tgfile = open("/../tieba-zhuaqu/reciveCache/tresult.txt","ab")
    for f in flist:
        fa = open("/../tieba-zhuaqu/reciveCache/"+f,"rb")
        data = fa.read()#.decode('utf8', 'ignore')
        #print(data)
        tgfile.write(data)
        fa.close()
        #os.system('sudo rm -rf ' + "/../tieba-zhuaqu/reciveCache/"+f)
    tgfile.close()


def CheckAdmin(relcmdA):
    for admincmd in TZDS.ADMIN_SETS:
        if relcmdA == admincmd:
            return True
    return False

    