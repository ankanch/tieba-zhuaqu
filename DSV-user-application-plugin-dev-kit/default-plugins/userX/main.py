from tkinter import *           # 导入 Tkinter 库
import tkinter.ttk as ttk
import userX
root = Tk()                  
root.resizable(False,False)
root.title("贴吧用户分析")

#KCC基本分析组件
#该组件用于统计特定用户的信息
##插件信息定义
KCC_PLUGIN_NAME="userX"
KCC_PLUGIN_DESCRIPTION="分析某位用户的发帖量，语句关键词"
KCC_PLUGIN_COPYRIGHT="kanch"
##定义结束

def btnclick():
    root.update()
    authorname = wordentry.get()
    SCALE = daysentry.get()
    scaletype = datascaleelem.get()
    print("authorname=",authorname,"\tSCALE=",SCALE,",\tscale type=",scaletype)
    if scaletype == "显示用户关系链":
        userX.userCircle(authorname)
    elif scaletype == "显示活跃度":
        userX.showLastDays(authorname,int(SCALE))
    elif scaletype == "显示语句关键词":
        userX.showKeyWord(authorname)
    elif scaletype == "活跃时间段分析":
        userX.activeTimeAnaylize(authorname,int(SCALE))
    else:
        print("出现未知错误：无法正常选择处理类型！")

def changetips(*args):
    scaletype = datascaleelem.get()
    if scaletype == "显示用户关系链":
        tipslabeldata.set("下面请留空")
    elif scaletype == "显示活跃度":
        tipslabeldata.set("要统计最近多少天的数据(0->all):")
    elif scaletype == "显示语句关键词":
        tipslabeldata.set("要统计最近多少天的数据(0->all):")
    elif scaletype == "活跃时间段分析":
        tipslabeldata.set("要统计最近多少天的数据(0->all):")
    else:
        tipslabeldata.set("要统计最近多少天的数据(0->all):")
    root.update()

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
tipslabeldata = StringVar(root)
Label(root,text="KCC数据分析模块 - 基本分析套件\n该模块用于从贴吧用户的维度分析一些基本数据",width=35,height=5).pack()
Label(root,text="请输入要分析的用户的ID:",width=25,height=2).pack()
wordentry = Entry(root,text="   ID",width=25,textvariable=data)
wordentry.pack(ipadx=4,ipady=4)
Label(root,text="分析类型:",width=25,height=2).pack()
variable = StringVar(root)
datascaleelem = ttk.Combobox(root, textvariable=variable, values=["天", "月", "年"],state='readonly')
datascaleelem["values"] = ("显示用户关系链", "显示活跃度", "显示语句关键词","活跃时间段分析")  
datascaleelem.current(1) 
datascaleelem.bind("<<ComboboxSelected>>",changetips) 
datascaleelem.pack()
tipslabeldata.set("要统计最近多少天的数据(<=0->all):")
tipslabel = Label(root,textvariable=tipslabeldata,width=30,height=2)
tipslabel.pack()
daysentry = Entry(root,text="请输统计最近多少天的",width=25,relief=GROOVE,textvariable=scale)
daysentry.pack(ipadx=4,ipady=4)
Button(root, text="显示结果", width=15,relief=GROOVE,command=btnclick).pack(pady=16,ipadx=8,ipady=8)

root = centerWindow(root)
root.mainloop()                 # 进入消息循环
