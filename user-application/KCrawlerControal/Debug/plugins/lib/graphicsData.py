# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
import numpy
font_set = FontProperties(fname=r"c:\\windows\\fonts\\simsun.ttc", size=15)  

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
    plt.xticks(lbwidth,xValueList,fontproperties=font_set)  
    rect = plt.bar(left = lbwidth,height = yValueList,width = xWidth,align="center",yerr=0.000001)  
    autolabel(rect)
    plt.show()
	
#折线图:蓝色粗线
def linePlotGraphics(xLabel,yLabel,xValueList,yValueList,graphicTitle='图例'):
    with plt.style.context('fivethirtyeight'):
        plt.title(graphicTitle,fontproperties=font_set)
        plt.xlabel(xLabel,fontproperties=font_set)
        plt.ylabel(yLabel,fontproperties=font_set)
        plt.xticks(numpy.arange(len(xValueList)),xValueList,rotation=45,fontproperties=font_set)    
        #plt.plot(xValueList,yValueList)
        plt.plot(yValueList)
        yValueList.sort()
    plt.subplots_adjust(bottom=0.15)
    plt.show()
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

#barGraphics('等级','数量',['A','B','C','D','E','F'],[29,30,40,47,38,23],'测试图例')
#linePlotGraphics("xLabel","yLabel",[1,2,3,4,5,6,7,8,9,10],[1.1,1.9,2.6,3.6,9.8,14,24,40,80,150],graphicTitle='图例')
#scatterPlotsGraphics("xLabel","yLabel",[1,2,3,4,5,6,7,8,9,10],[1,11.9,2,6.3,6,9.8,14,4,8,5],graphicTitle='图例')