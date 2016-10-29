#encoding=utf-8
import socket  
import shareLib.TZDatagramSymbol as symbol

#Simple Internet Communication class
class SIC:    
    s = 0
    ip = ""
    port = 0  

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP

    #def __del__(self):
     #   conn.close()

    def setInfo(self,IP,PORT):
        self.ip = IP
        self.port = PORT

    def startServer(self,accept_count=1):
        self.s.bind((self.ip,self.port))   #套接字绑定的IP与端口
        self.s.listen(accept_count)         #开始TCP监听

    def waitForConnection(self):
        conn,addr = self.s.accept()   #接受TCP连接，并返回新的套接字与IP地址
        return  conn,addr

    def recvData(self,conn,size=1024):
        data = conn.recv(size)    #把接收的数据实例化
        data = data.decode("utf-8")
        return data

    def sendData(self,conn,data):
        conn.sendall(data.encode("utf-8"))

    def closeSocket(self): 
        self.s.close()

#the 3 function below used as globe function to recv data and send data and control a connection
def clientInterreactiveRecv(conn,size=1024):
    data = conn.recv(size)  
    #data = data.decode("utf-8",'ignore')
    data = data.decode("utf-8")
    return data

def clientInterreactiveSend(conn,data):
    conn.sendall(data.encode("utf-8"))

def clientInterreactiveRecvNOENCODE(conn,size=1024):
    data = conn.recv(size)  
    return data

def clientInterreactiveSendNOCODE(conn,data):
    conn.sendall(data)

def closeConnection(conn):
    conn.close()


#一次握手函数
def shakeHand(crawlerdata,cmd="502,connection test"):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((crawlerdata[1],int(crawlerdata[2]))) #ID,IP,PORT
        s.sendall(cmd.encode("utf-8"))  
        data=s.recv(1024)
        data = data.decode("utf-8")
        print("\t\t\tcrawler #",crawlerdata[0],":",data)    
        s.close()
        return True
    except Exception as e:
        print(e)    
        return False

