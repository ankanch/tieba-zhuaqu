from tkinter import *           # 导入 Tkinter 库
import tkinter.ttk as ttk
import wordstimeliner
root = Tk()                  
root.resizable(False,False)
root.title("时间频率图")

#KCC基本分析组件
#该组件用于统计某个词语的频率变化并以折线统计图的形式显示
##插件信息定义
KCC_PLUGIN_NAME="WordTimeliner"
KCC_PLUGIN_DESCRIPTION="显示指定词语的时间频率图"
KCC_PLUGIN_COPYRIGHT="kanch"
##定义结束

def btnclick():
    root.update()
    word = wordentry.get()
    SCALE = daysentry.get()
    scaletype = datascaleelem.get()
    print("word=",word,"\tSCALE=",SCALE,",\tscale type=",scaletype)
    if scaletype == "天":
        wordstimeliner.showLastDays(word,int(SCALE))
    elif scaletype == "月":
        wordstimeliner.showLastMonths(word,int(SCALE))
    elif scaletype == "年":
        wordstimeliner.showLastYears(word,int(SCALE))
    else:
        print("出现未知错误：无法正常选择日期！")

def centerWindow(rt):
    rt.update() # update window ,must do
    curWidth = rt.winfo_reqwidth() # get current width
    curHeight = rt.winfo_height() # get current height
    scnWidth,scnHeight = rt.maxsize() # get screen width and height
    # now generate configuration information
    tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,
    (scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
    rt.geometry(tmpcnf)
    return rt
    
data = StringVar(root)
scale = IntVar(root)
Label(root,text="KCC数据分析模块 - 基本分析套件\n该模块用于显示指定词语的时间频率关系图",width=35,height=5).pack()
Label(root,text="请输入要分析的词语（仅一个）:",width=25,height=2).pack()
wordentry = Entry(root,text="请输入内容",width=25,textvariable=data)
wordentry.pack(ipadx=4,ipady=4)
Label(root,text="数据精细程度:",width=25,height=2).pack()
variable = StringVar(root)
datascaleelem = ttk.Combobox(root, textvariable=variable, values=["天", "月", "年"],state='readonly')
datascaleelem["values"] = ("天", "月", "年")  
datascaleelem.current(0)  
#datascaleelem.bind("<<ComboboxSelected>>", getScaleElem)  
datascaleelem.pack()
Label(root,text="请输入显示最近多少天的统计图:",width=25,height=2).pack()
daysentry = Entry(root,text="请输显示多少天的",width=25,relief=GROOVE,textvariable=scale)
daysentry.pack(ipadx=4,ipady=4)
Button(root, text="获取edit内容", width=15,relief=GROOVE,command=btnclick).pack(pady=16,ipadx=8,ipady=8)

root = centerWindow(root)
root.mainloop()                 # 进入消息循环
