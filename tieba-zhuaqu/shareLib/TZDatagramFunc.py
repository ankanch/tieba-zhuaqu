import shareLib.TZDatagramSymbol as symbol
import shareLib.TZInternetCommunication as TZIC

#this function used to find matched cmd to a specific cmd
def findMatchCommand(cmd):
    for command in symbol.CMD_MAP:
        if command[0] == int(cmd.split(",")[0]):
            return command[1]
    return symbol.ERROR

#this function used to reslove cmds
def resolveCommand(cmd):
    dta = cmd.split(",")
    dta[0] = int(dta[0])
    return dta

#this function used to make up cmd
def makeUpCommand(head,parameters):
    head = str(head)
    for item in parameters:
        head = head + "," + str(item)
    return head

#这个函数用获取期望的响应,获取成功则返回得到的整条命令
def getPerferResponse(perferResponseCode,conn):
    data = TZIC.clientInterreactiveRecv(conn)
    data = resolveCommand(data)
    if data[0] == perferResponseCode:
        return True,data
    else:
        return False,"NO_PERFER"