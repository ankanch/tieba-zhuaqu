import lib.result_functions_file as RFF
import lib.maglib as MSG
import os


#这个库是统计各个词语的出现次数，并显示
#这是tieba-zhuaqu项目的用户端基本插件
#该函数用于统计各个词语的出现次数
#函数返回：一个任意字符串和指定词语的出现次数
def satisticWord(word):
    os.system('cls')
    print('>>>>>开始统计【',word,'】出现次数....')
    sum=1
    mlist=[]
    mlist = RFF.queryWordContainList(word)
    sum = len(mlist)
    print('>>>>>统计完成！\n\n')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',0,'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    for item in mlist:
        try:
            print('\t◆\t',item[0])
        except Exception as e:
            print('\t◆\t<<无法编码字符>>')
    MSG.printline2x35(2)
    print('\r\n>>>>>统计结果>----->共【',sum-1,'/',0,'】条匹配数据，结果如下','\r\n')
    MSG.printline2x35(2)
    return 'SW',sum-1