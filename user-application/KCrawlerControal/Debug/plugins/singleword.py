import lib.result_functions_file as RFF
import lib.maglib as MSG
import os


#这个库是统计各个词语的出现次数，并显示
#这是tieba-zhuaqu项目的用户端基本插件
def satisticWord(word,datalist):
    os.system('cls')
    print('>>>>>开始统计【',word,'】出现次数....')
    sum=1
    mlist=[]
    for item in datalist:
        if item.find(word) != -1:
            sum+=1
            mlist.append(item)
        print('>',end='')
    print('>>>>>统计完成！\n\n')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',len(datalist),'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    for item in mlist:
        print('\t◆\t',item)
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',len(datalist),'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    return 'SW',sum-1

satisticWord(input("请输入要统计的词语："),RFF.getContentList())