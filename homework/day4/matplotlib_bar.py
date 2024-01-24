#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] =['SimHei']   #设置中文
plt.rcParams['font.family'] = 'sans-serif' #

def mat_bar(name_list, count_list,title,x_label,y_label,color_list):
    #调节图形大小，宽，高
    plt.figure(figsize=(6,6))

    #横向柱状图
    # plt.barh(name_list, count_list, width=0.5,color=color_list)
    #竖向柱状图
    plt.bar(name_list, count_list, width=0.5,color=color_list)

    #添加主题和注释

    plt.title(title)  #主题
    plt.xlabel(x_label)  #X轴注释
    plt.ylabel(y_label)  #Y轴注释

    #保存到图片
    # plt.savefig('result2.phg')

    #绘制图形
    plt.show()



if __name__ == "__main__":
    name_list = ['name1', 'name2', 'name3', 'name4']
    count_list =[123, 555, 354, 800]
    bar_name = '2023销售状况'
    x_label = '月份'
    y_label = '万'
    colors = ['red', 'blue', 'green', 'yellow']
    mat_bar(name_list, count_list,bar_name,x_label,y_label,colors)