import os,sys
import pickle
import maglib as MSG
import jieba
import jieba.analyse
import graphicsData as drawGraphic

GV_DATALIST_SUM = [0]

def startPocessMoudle(result_list):
    f = open('C:\\ktieba\\result_add','rb')
    xs = pickle.load(f)
    f.close()
    GV_DATALIST_SUM[0] = xs['sum']
    menu(result_list)

def showCopyRight(result_list):
    copyrightinfo = """
    =======================================
    本程序用来对抓取贴吧帖子的标题进行分析。
    可以实现词频统计，指定关键词寻找帖子数目。
    可以显示基本的柱形统计图来对比数据
    =======================================
    本程序使用jieba中文分词模块
    详情：https://github.com/fxsjy/jieba
    =======================================
    by kanch@0/828/16emo/h
    kanchisme@gmail.com
	=======================================
	其它模块说明：
	maglib       ： 用来输出分隔符
	tieba-title  ：下载网页，抓取标题的主要模块
	dataminer    ：提取关键字，进行统计的主要模块
	graphicsData ：绘图模块（对matplotlib函数进行初步封装）
	=======================================
    """

    os.system('cls')
    print (copyrightinfo)
    MSG.printline22x35(2)
    nextopt(result_list)

def menu(result_list):
    os.system('cls')
    MSG.printline2x35(2)
    print('\n\n\n\n\t\t本模块可以用来对抓取结果进行初步处理，请选择需要进行的操作')
    print('\t\t数据源：',result_list)
    print('\n\n\n\t\t【1】.指定词语统计\n\t\t【2】.显示高频词语\n\t\t【3】.忽略词选项\n\t\t【4】.对比统计多个词语\n\n\t\t【0】.退出程序\n\t\t【9】.关于本程序','\r\n\r\n')
    MSG.printline2x35(2)
    opt = input('\n\n\t\t请输入操作代号：_____\b\b\b')
    if( int(opt) == 1 ):
        word = input('\n\t\t请输入要统计的词语：______\b\b\b\b')
        satisticWord(word,result_list)
    elif int(opt) == 2:
        showHFW(result_list)
    elif int(opt) == 3:
        ignoreWord(result_list)
    elif int(opt) == 4:
        compareWords(result_list)
    elif int(opt) == 0:
        sys.exit()
    elif int(opt) == 9:
        showCopyRight(result_list)
    else:
        os.system('cls')
        print('>>>>>未找到匹配操作代号，请重新输入！')
        menu(result_list)

def resta(result_list):
    os.system('cls')
    word = input('\n\t\t请输入要统计的词语：______\b\b\b\b')
    satisticWord(word,result_list)

def nextopt(result_list):
    opt = '000'
    while opt != 'EXIT':
        if opt == 'MENU':
            menu(result_list)
        opt = input('>>>>>您可以输入 EXIT 退出程序，或者 MENU 返回上级菜单\n>>>>>请选择：____\b\b\b')


def satisticWord(word,result_list):
    os.system('cls')
    print('>>>>>开始统计【',word,'】出现次数....')

    f = open(result_list,'rb')
    data = f.read()
    f.close()
    data = data.decode('gbk', 'ignore')
    datalist = data.split('\r\n\t\t')
    sum=1
    mlist=[]
    for item in datalist:
        if item.find(word) != -1:
            sum+=1
            mlist.append(item)
        print('>',end='')
    print('>>>>>统计完成！\n\n')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',GV_DATALIST_SUM[0],'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    for item in mlist:
        print('\t◆\t',item)
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',GV_DATALIST_SUM[0],'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    return 'SW',sum-1



def showHFW(result_list):
    f = open(result_list,'rb')
    data = f.read()
    f.close()
    data = data.decode('gbk', 'ignore')
    datalist = data.split('\r\n\t\t')
    dictHFW = {}
    os.system('cls')
    print('>>>>>载入忽略词列表....')
    f = open('C:\\ktieba\\ignoreWords','rb')
    orglist = pickle.load(f)
    #print(orglist)
    f.close()
    print('>>>>>载入成功！')
    print('>>>>>开始处理，调用jieba分词....')
    for item in datalist:
        seg_list = jieba.cut(item, cut_all=True)
        for si in seg_list:
            if len(si) > 1:
                if si not in orglist :
                    if si in dictHFW:
                        dictHFW[si] = dictHFW[si] + 1
                    else:
                        dictHFW[si] = 1
    dictHFW= sorted(dictHFW.items(), key=lambda d:d[1], reverse = True)

    howmany = input('>>>>>程序处理完毕，请输入要显示多少高频词语(共'+ str(len(dictHFW)) +'个词语)：________\b\b\b\b\b')
    os.system('cls')
    MSG.printline2x35(2)
    print('>>>>处理完毕，结果如下')
    MSG.printline2x35(2)
    x = 0
    for k in dictHFW:
        print(str(k),end='\t\t')
        x += 1
        if x % 4 == 0:
            print('\r\n')
        if x >= int(howmany):
            break
        
    print('\r\n')
    MSG.printline2x35(2)
    print('>>>>处理完毕，结果如上')
    MSG.printline2x35(2)
    
    
    opt = '000'
    while opt != 'EXIT':
        if opt == 'MENU':
            menu(result_list)
        elif opt == 'ADDIW':
            addIgnoreWords()
        opt = input('>>>>>统计完成，您可以输入 EXIT 退出程序，或者 MENU 返回上级菜单\n>>>>>也可以输入ADDIW 添加忽略词（不会显示在统计结果中）\n>>>>>请选择：____\b\b\b')

def ignoreWord(result_list):
    os.system('cls')
    MSG.printline2x35(2)
    print('\t\t【1】.查看现有忽略词\n\t\t【2】.增加忽略词\n\t\t【3】.删除忽略词语\n\n\t\t【0】返回上一级')
    opt = input('\t\t请输入操作代码：________\b\b\b\b\b')
    ip = int(opt)
    if ip == 1:
        showIWs(result_list)
    elif ip == 2:
        addIgnoreWords()
    elif ip == 3:
        delIWs(result_list)
    elif ip == 0:
        menu()
    else:
        print('>>>>>操作代码无效，请重新输入！')
        ignoreWord(result_list)

def showIWs(result_list):
    f = open('C:\\ktieba\\ignoreWords','rb')
    orglist = pickle.load(f)
    f.close()
    MSG.printline2x35(2)
    print('>>>>当前存在的忽略词列表如下：')
    MSG.printline2x35(2)
    t = 0
    for item in orglist:
        print(item,end='\t\t')
        t += 1
        if t % 5 == 0 :
            print('\r\n')
    print('\r\n')
    nextopt(result_list)

def delIWs(result_list):
    f = open('C:\\ktieba\\ignoreWords','rb')
    orglist = pickle.load(f)
    f.close()
    MSG.printline2x35(2)
    print('>>>>当前存在的忽略词列表如下：')
    MSG.printline2x35(2)
    t = 0
    for item in orglist:
        print(item,end='\t\t')
        t += 1
        if t % 5 == 0 :
            print('\r\n')
    print('\r\n请输入要删除的词语，多个词语请用空格隔开：')
    words = input('>>>>> ')
    wl = words.split()
    for item in wl:
        if item in orglist:
            orglist.remove(item)
    f = open('C:\\ktieba\\ignoreWords','wb')
    pickle.dump(orglist, f,2)
    f.close()
    MSG.printline2x35(2)
    print('>>>>删除完毕！')
    MSG.printline2x35(2)
    nextopt(result_list)

def addIgnoreWords():
    f = open('C:\\ktieba\\ignoreWords','rb')
    orglist = pickle.load(f)
    f.close()
    MSG.printline2x35(2)
    print('>>>>请在下面输入要忽略的词语，被忽略的词语将不会显示在高频词语统计中（多个词语请用空格分开,仅记录长度大于2的词）:')
    words = input('>>>>> ')
    wlist = words.split()
    for item in wlist:
        if len(item) > 1:
            orglist.append(item)
            #print(item)
    f = open('C:\\ktieba\\ignoreWords','wb')
    pickle.dump(orglist, f,2)
    f.close()
    

#比较函数
def compareWords(result_list):
    print('>>>>>多关键字比较，请输入多个关键字（以空格分隔），程序将会统计它们出现次数并绘制柱形统计图')
    words = input('>>>>> ')
    wordlist = words.split()
    countlist = []
    tp = 'null'
    cd = 0
    print('>>>>>开始处理.....')
    for item in wordlist:
        tp,cd = satisticWord(item,result_list)
        countlist.append(cd)
    print('>>>>>处理完成，加载图像中.....')
    print('>>>>>图像加载完毕')
    drawGraphic.barGraphics('关键字（帖子总数：'+str(GV_DATALIST_SUM[0])+')','出现次数',wordlist,countlist,'指定关键字在帖子标题中的出现次数对比')
    nextopt(result_list)



