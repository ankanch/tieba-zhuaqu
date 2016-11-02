import threading 
import os
import shareLib.TZInternetCommunication as TZIC
import shareLib.TZDatagramSymbol as TZDS 
import shareLib.TZDatagramFunc as TZDF
import shareLib.TZautoInteractFunc as TZIF

#SERVER_HOST = "216.45.55.153"   #private python VPS
SERVER_HOST = "172.31.24.123"    #amazon ECS
SERVER_PORT = 50005

def showMsg(msg):
    print("TZ TaskManager:",msg)

#对于每一个新连接进来的客户端，都调用这个进行交互
def Interactive(conn,ct,nct,crawlist):
    TZIC.clientInterreactiveSend(conn,"TiebaZhuaqu TaskManager ver1.0 by Kanch\nkanchisme@gmail.com\nhttp://lucky1965.xyz\n")
    TZIF.setDate(TZDS.DATA_CRAWLER_STATUS,0.0,int(nct))
    FIRSTRUN = True
    ADMINCONVERSITION = False
    IS_ADMIN = False  #用来关闭回显
    while 1:
        data = TZIC.clientInterreactiveRecv(conn)
        if len(data) < 3:
            if ADMINCONVERSITION == True:
                print("Admin conversition offline.")
                break
            else:
                print("conversiton interrupted!")
                break
        cmd = TZDF.findMatchCommand(data)
        relcmd = TZDF.resolveCommand(data)
        IS_ADMIN = TZIF.CheckAdmin(int(relcmd[0]))
        if FIRSTRUN == True:
            if TZIF.CheckAdmin(int(relcmd[0])) == True:
                ADMINCONVERSITION = True
        if(int(relcmd[0]) != TZDS.ADMIN_JOBCREATE and IS_ADMIN == False ):
            showMsg("\tInteractive:Client #"+ str(ct+1) +":"+ str(data))
            print("\t\t\tInteractive:relcmd",relcmd)
        else:
            print("JOB RECIVED!")
        if(int(relcmd[0]) == TZDS.FINISH ):
            break
        elif( int(relcmd[0]) == TZDS.OFFLINE ):
            xc = 0
            BK = False
            for item in crawlist:  #ID,IP,PORT
                print("item[0]=",item[0],"nct=",nct)
                if int(item[0]) == int(nct):
                    del crawlist[xc]
                    BK = True
                    break
                xc += 1
            TZIF.delData(TZDS.DATA_CRAWLER_STATUS,int(nct))
            TZIF.setDate(TZDS.CRAWLER_LIST,crawlist)
            if BK == True:
                break
        elif(int(relcmd[0]) == TZDS.ADMIN_SHUTDOWN):
            SERVER_SHUTDOWN[0] = True
            break
        cmd = TZIF.autoInteract(relcmd,conn,nct,crawlist)
        TZIC.clientInterreactiveSend(conn,str(cmd))
    TZIC.closeConnection(conn)
    del t[nct]
    count[0]-=1
    if( IS_ADMIN == False):
        showMsg("*********************\r\n***\t***Client #"+ str(ct+1) +": connection closed,resource cleaned***\r\n*********************")


os.system('clear')
#程序主逻辑代码
sic = TZIC.SIC()   #网络操作对象

#关键变量
CRAWLER_LIST = []   #存放当前已经连线的爬虫  #ID,IP,PORT,connection socket

showMsg("initial service...")
t = {}
numbercount = 0
count = []
count.append(0)
SERVER_SHUTDOWN = []
SERVER_SHUTDOWN.append(False)
TZIF.InitDataExchangeTZautoInteractFunc()   
sic.setInfo(SERVER_HOST,SERVER_PORT)
showMsg("starting server...")
sic.startServer(10)
showMsg("server started successfully\twating for connection...")
while 1:
    conn,addr = sic.waitForConnection()
    showMsg("new client connect!" + "<client number =" + str(count[0]+1))
    tn = threading.Thread(target=Interactive,args=(conn,count[0],numbercount,CRAWLER_LIST,))
    t[numbercount] = tn
    t[numbercount].setDaemon(True)
    t[numbercount].start()
    numbercount+=1
    showMsg("client thread has been created and start running!")
    count[0]+=1
    if(SERVER_SHUTDOWN[0]):
        break
sic.closeSocket()
showMsg("server now has been shutdown")
