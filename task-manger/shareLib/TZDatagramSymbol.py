#command definations
    #Public 
OK = 666                        #reply for TEST
OKCLOSE = 668                   #close reply
TEST = 661                      #online test
FACTORY_TEST = 700              #for debug
ERROR = 660                     #when unknow command recived
FINISH = 662                    #inform server to disconnect
    #Crawler
REGISTE = 101                   #registe a crawler to server
OFFLINE = 102                   #inform server crawler is going offline
JOBSTATUS = 103                 #sned job status to a server
JOBTRANSFER = 104               #transfer result file to server when a job finished 

    #Admin
ADMIN_STATUS = 301              #query total job pocessing status (rates)
ADMIN_CRAWLER_LIST = 302        #query a list of all the crawler that online
ADMIN_JOBCREATE = 303           #inform  server a job has been created
ADMIN_JOBTRANSFER = 304         #inform server to send result file when all the sub job finished
ADMIN_SHUTDOWN = 305            #shutdown the TaskManager
ADMIN_ONLINE = 306              #inform server adming is online

    #Server
START_TRANSFER = 501            #inform the client that server start send result file
ONLINE_ECHO = 502               #when   REGISTE and ADMIN_ONLINE recived,send this 
JOB_CONFIRM = 503               #when a ADMIN_JOBCREATE recived,send this to comfirm
JOB_ALLOCATION = 505                  #server allocate job to crawler when this send
CRAWLER_LIST = 504              #use this to send a CRAWLER_LIST


CMD_MAP = [
    (TEST,OK),
    (FINISH,OKCLOSE),
    (REGISTE,ONLINE_ECHO),
    (JOBSTATUS,OK),
    (JOBTRANSFER,OK),
    (ADMIN_STATUS,OK),
    (ADMIN_CRAWLER_LIST,CRAWLER_LIST),
    (ADMIN_JOBCREATE,JOB_CONFIRM),
    (ADMIN_JOBTRANSFER,START_TRANSFER),
    (ADMIN_SHUTDOWN,OKCLOSE),
    (ADMIN_ONLINE,ONLINE_ECHO)
]


ADMIN_SETS = [
    ADMIN_STATUS,       
    ADMIN_CRAWLER_LIST,
    ADMIN_JOBCREATE,     
    ADMIN_JOBTRANSFER,  
    ADMIN_SHUTDOWN ,  
    ADMIN_ONLINE 
]


#下面的符号为TZsutoInteractFunc中setData和fetData函数所用
DATA_TOTAL_AVERAGE_STATUS = "DATA_TOTAL_AVERAGE_STATUS"         #DATA_TOTAL_AVERAGE_STATUS
DATA_CRAWLER_STATUS = "DATA_CRAWLER_STATUS"                     #DATA_CRAWLER_STATUS

DATA_POCESS_TIEBA_NAME = "DATA_POCESS_TIEBA_NAME"               #code for tieba name to capture
DATA_POCESS_PAGES_TO = "DATA_POCESS_PAGES_TO"                   #code for how many page to capture

DATA_CRAWLER_LIST = "DATA_CRAWLER_LIST"                         #code for crawler list storage


#ESSENTIAL DATA this used to identify a admin
ESSEN_ADMIN_CODE = "TEST"