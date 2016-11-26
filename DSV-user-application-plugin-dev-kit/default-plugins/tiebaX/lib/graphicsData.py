# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
import numpy
import os
font_set = FontProperties(fname=r"c:\\windows\\fonts\\simsun.ttc", size=15)  


#重要全局变量
PATH_SUFFIX = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
PATH_SUFFIX+="\\userX\\"   #插件根目录

#基本柱形统计图
def barGraphics(xLabel,yLabel,xValueList,yValueList,graphicTitle='图例',xWidth=0.5):
    lbwidth = []
    x = 1
    for item in xValueList:
        lbwidth.append(x)
        x += xWidth
    plt.title(graphicTitle,fontproperties=font_set)
    plt.xlabel(xLabel,fontproperties=font_set)
    plt.ylabel(yLabel,fontproperties=font_set)  
    plt.xticks(lbwidth,xValueList,rotation=25,fontproperties=font_set)  
    rect = plt.bar(left = lbwidth,height = yValueList,width = xWidth,align="center",yerr=0.000001)  
    autolabel(rect)
    plt.show()

#水平统计图
def barHonGraphics(xLabel,yLabel,xValueList,yValueList,graphicTitle='图例',xWidth=0.5):
    plt.barh(numpy.arange(len(xValueList)), yValueList, alpha=0.4)
    plt.yticks(numpy.arange(len(xValueList)), xValueList,fontproperties=font_set)
    plt.xlabel(yLabel,fontproperties=font_set)
    plt.ylabel(xLabel,fontproperties=font_set)
    plt.title(graphicTitle,fontproperties=font_set)

    plt.show()
	
#折线图:蓝色粗线
def linePlotGraphics(xLabel,yLabel,xValueList,yValueList,graphicTitle='图例'):
    with plt.style.context('fivethirtyeight'):
        plt.title(graphicTitle,fontproperties=font_set,fontsize=20)
        plt.xlabel(xLabel,fontproperties=font_set)
        plt.ylabel(yLabel,fontproperties=font_set)
        plt.xticks(numpy.arange(len(xValueList)),xValueList,rotation=45,fontproperties=font_set)    
        plt.plot(yValueList)
        yValueList.sort()
    #设置y轴区间以及图像最低端距x轴距离
    print("len(yValueList)=",len(yValueList))
    plt.ylim(-1.0, yValueList[len(yValueList)-1]+1)
    plt.subplots_adjust(bottom=0.15,left=0.05,right=0.98,top=0.92)
    #下面的代码用来设置网格线
    ax = plt.gca()
    ax.get_xaxis().tick_bottom() #仅显示下面的x轴的ticks
    ax.get_yaxis().tick_left()
    ax.grid(b=False,axis='x')
    axis = ax.xaxis
    for line in axis.get_ticklines():
        line.set_color("gray")
        line.set_markersize(6)
        line.set_markeredgewidth(1)
    #显示折线图
    plt.show()
    #plt.savefig('percent-bachelors-degrees-women-usa.png', bbox_inches='tight')
#散点图:蓝色点
def scatterPlotsGraphics(xLabel,yLabel,xValueList,yValueList,graphicTitle='图例'):
    with plt.style.context('fivethirtyeight'):
        plt.plot(xValueList, yValueList,'o')
    plt.show()


#用来显示柱形图顶部的数字标识
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % int(height))

#饼状图
def pieGraphics(Labels,ValueList,graphicTitle='图例'):
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', "blue","green","cyan","magenta"]
    maxdata = max(ValueList)
    explode = []
    for v in ValueList:
        if v == maxdata:
            explode.append(0.1)
        else:
            explode.append(0)
    print(explode)
    patches,l_text,p_text = plt.pie(ValueList, labels=Labels, colors=colors,autopct='%1.1f%%',explode=explode ,shadow=True, startangle=90)
    for font in l_text:
        font.set_fontproperties(FontProperties(fname=PATH_SUFFIX+'SIMLI.TTF'))
    plt.title(graphicTitle,fontproperties=font_set,y=1.05)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()
