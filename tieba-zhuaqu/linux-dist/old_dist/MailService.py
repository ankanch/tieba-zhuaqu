#coding:utf-8  #强制使用utf-8编码格式
import smtplib #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
my_sender='kanchpybot@163.com' #发件人邮箱账号，为了后面易于维护，所以写成了变量
my_sender_password = "XYZ2016python"  #发件人邮箱
#my_user='1075900121@qq.com' #收件人邮箱账号，为了后面易于维护，所以写成了变量

#This function send mail use kanchpybot@163.com
def SendMail(TO,TITLE,CONTENT):
    ret = Mail(TO,TITLE,CONTENT)
    if ret:
        print("Mail sent success!") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
    else:
        print("Failed to sent mail!") #如果发送失败则会返回filed

def Mail(TO,TITLE,CONTENT):
  ret=True
  my_user = TO
  try:
    msg=MIMEText(CONTENT,'plain','utf-8')
    msg['From']=formataddr(["Kanch's PythonBot @ MyPythonVPS",my_sender])  #括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To']=formataddr(["Autosend by bot",my_user])  #收件人邮箱昵称、收件人邮箱账号
    msg['Subject']=TITLE #邮件的主题
 
    server=smtplib.SMTP("smtp.163.com",25) #发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender,my_sender_password)  #括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender,my_user,msg.as_string())  #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit() 
  except Exception:  
    ret=False
  return ret
 
#SendMail("1075900121@qq.com",'主题','括号中对应的是发件人邮箱账号、括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件邮箱密码')
