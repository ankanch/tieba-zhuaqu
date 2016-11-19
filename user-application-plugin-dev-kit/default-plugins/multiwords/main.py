from tkinter import *           # 导入 Tkinter 库
import multiwords
root = Tk()                  
root.resizable(False,False)
root.title("统计对比多个词语")

#KCC基本分析组件
#该组件用于列举出包含指定词语的帖子/回帖
##插件信息定义
KCC_PLUGIN_NAME="multiwordS"
KCC_PLUGIN_DESCRIPTION="用来统计多个词语的频率并以条形统计图显示"
KCC_PLUGIN_COPYRIGHT="kanch"
##定义结束

def btnclick():
    root.update()
    wordlist = wordentry.get()
    print("word=",wordlist)
    multiwords.compareMultiWords(wordlist)

def centerWindow(rt):
    rt.update() # update window ,must do
    curWidth = rt.winfo_reqwidth() # get current width
    curHeight = rt.winfo_height() # get current height
    scnWidth,scnHeight = rt.maxsize() # get screen width and height
    tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,
    (scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    rt.geometry(tmpcnf)
    return rt

data = StringVar(root)
scale = IntVar(root)
Label(root,text="KCC数据分析模块 - 基本分析套件\n该模块用于显示指定词语的时间频率关系图",width=35,height=5).pack()
Label(root,text="请输入要分析的词语（用空格隔开）:",width=25,height=2).pack()
wordentry = Entry(root,text="请输入内容",width=25,textvariable=data)
wordentry.pack(ipadx=4,ipady=4)
Button(root, text="显示结果", width=15,relief=GROOVE,command=btnclick).pack(pady=16,ipadx=8,ipady=8)

root = centerWindow(root)
root.mainloop()                 # 进入消息循环
