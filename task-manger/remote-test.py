import socket
import os
import shareLib.TZDatagramSymbol as TZDS
import shareLib.TZautoInteractFunc as TZIF
import shareLib.TZDatagramFunc as TZDF
import shareLib.TZInternetCommunication as TZIC

HOST='216.45.55.153'
PORT=50005
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CS = True
while CS:
    try:
        s.connect((HOST,PORT))
        CS = False
    except Exception as e:
        print(e)  

localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
LOCAL_PORT = 50006
os.system('cls')
print ("local ip:",localIP)
data=s.recv(1024)  
print("Remote Server(TM):",data.decode("utf-8"))
cmd = "123"
STATUS = 0  #0=ok,1=file send mode ,2 = regist
ID = -1
registcmd = "101," + str(localIP) + ",50006"
s.sendall(registcmd.encode("utf-8"))  
data=s.recv(1024)  
data = data.decode("utf-8")
CID = TZDF.resolveCommand(data)[1]
CID = int(CID)   #得到分配的ID
if CID < 0 :
    print("remote server cannot  allocate ID,applicaiton will exit!")
    exit()
print("ID=",CID)
while cmd != "SHUTDOWN":
    data=s.recv(1024)  
    if(STATUS == 0):
        print("Remote Server(TM):",data.decode("utf-8"))
    elif(STATUS == 1):
        print("Remote Server(TM):",data.decode("utf-8"))
        TZIF.sendFile(s,crawlerid=ID)
        STATUS = 0
    elif(STATUS == 2):
        data = data.decode("utf-8")
        relcmd = TZDF.resolveCommand(data)
        CLIST = str(relcmd[1])
        CLIST = CLIST.replace("@@",",")
        print(str(CLIST))
        STATUS = 0
    elif STATUS == 3:
        data = data.decode("utf-8")
        print("Remote Server(TM):",data)
        cmd = input("confirm job?____\b\b\b")
        TZIC.clientInterreactiveSend(s,cmd)
        print("waiting for response...")
        cmd = TZIC.clientInterreactiveRecv(s)
        print("Remote Server(TM):",cmd)
        STATUS = 0
    elif STATUS == 4:
        TZIF.recvFileAdmin(s)
        cmd = TZIC.clientInterreactiveRecv(s)
        print("Remote Server(TM):",cmd)
        STATUS = 0
    cmd = input("Please input cmd:")
    s.sendall(cmd.encode("utf-8"))  
    print('data sended!')
    cmd = TZDF.resolveCommand(cmd)
    cmd  = str(cmd[0])
    if cmd == "662" or cmd == "305" or cmd == "102":
        if cmd == "102" :
            data=s.recv(1024)
            print("Remote Server(TM):",data.decode("utf-8"))
        break;   
    elif cmd == str(TZDS.JOBTRANSFER):
        #send file  104
        STATUS = 1
    elif cmd == str(TZDS.ADMIN_CRAWLER_LIST):
        #get crawler list 302
        STATUS = 2
    elif cmd == str(TZDS.ADMIN_JOBCREATE):
        #303 create job by admin
        STATUS = 3
    elif cmd == str(TZDS.ADMIN_JOBTRANSFER):
        #304
        STATUS = 4


print("Connection has been closed!")      
s.close()
