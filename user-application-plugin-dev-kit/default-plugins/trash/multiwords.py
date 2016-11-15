import lib.result_functions_file as RFF
import lib.maglib as MSG
import lib.graphicsData as drawGraphic

#这个库是用来对比统计多个词语并以柱形统计图的形式显示
#这是tieba-zhuaqu项目的用户端基本插件
def compareMultiWords(datalist):
    print('>>>>>多关键字比较，请输入多个关键字（以空格分隔），程序将会统计它们出现次数并绘制柱形统计图')
    words = input('>>>>> ')
    wordlist = words.split()
    countlist = []
    tp = 'null'
    cd = 0
    print('>>>>>开始处理.....')
    for item in wordlist:
        tp,cd = RFF.satisticWord(item,datalist)
        countlist.append(cd)
    print('>>>>>处理完成，加载图像中.....')
    drawGraphic.barGraphics('关键字（帖子/回帖总数：'+str(len(datalist))+')','出现次数',wordlist,countlist,'指定关键字在帖子标题中的出现次数对比')
    print('>>>>>图像加载完毕')
compareMultiWords(RFF.getContentList())