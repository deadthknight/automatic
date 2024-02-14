#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

# import matplotlib      #linux
#
# matplotlib.use('agg')  # linux
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.rcParams['font.family'] = 'sans-serif'  #


def mat_line(lines_list, title, x_label, y_label):
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))

    # 一共一行，每行一图，第一图
    ax = fig.add_subplot(111)

    # 处理X轴时间格式

    import matplotlib.dates as mdate

    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S')) #设置时间标签显示格式

    # 处理Y轴百分比格式
    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%3.1f%%'))

    # # 设置Y轴范围为0到100
    plt.ylim(0, 100)
    # # 设置Y轴刻度为0到100，每10为一个刻度
    # plt.yticks(range(0, 101, 10))

    # 添加主题和注释

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # 当X轴太拥挤的时候可以让他自适应
    fig.autofmt_xdate()

    # 循环x_y_list, 提取多线条的数据，并绘图
    # [[x_list, y_list, line_style,color,line_name], [x_list, y_list, line_style,color,line_name]]
    for x_list, y_list, line_style, color, line_name in lines_list:
        # --------每一条线的数据---------
        # x_list         :X轴数据
        # y_list         :Y轴数据
        # line_style     :线类型(solid：实线)(dashed:虚线)
        # color          :线颜色
        # line_name      :线名称
        ax.plot(x_list, y_list, linestyle=line_style, color=color, label=line_name)

    # 设置说明的位置
    ax.legend(loc='upper left')

    # 保持到图片
    # plt.savefig('result_linear.png')

    # 绘制图形
    plt.show()


if __name__ == "__main__":
    from datetime import datetime, timedelta
    from random import random, choice

    # 想产生的线的数量
    line_no = 2
    # 线产生的线的数据点数量
    data_points_count = 10
    # 线的颜色列表，随机选择
    color_list = ['red', 'blue', 'green', 'yellow']

    # 线的的类型列表，随机选择
    line_style_list = ['solid', 'dashed']

    # 当前时间，数据点会持续加分钟数
    now = datetime.now()

    # 最终的拥有多条线数据的列表
    lines_list = []

    # 随机产生多线数据列表的循环
    for l in range(line_no):
        # 每条线的名称
        line_name = f"line{l+1}"
        # 每条线的X轴数据列表
        line_x_list = []
        # 每条线的Y轴数据列表
        line_y_list = []
        # 写入每条线的数据列表
        for d in range(data_points_count):
            # 写入X轴的时间，在now基础之上加分钟数
            line_x_list.append(now + timedelta(minutes=d))
            # 写入Y轴的百分比，随机在1-100直接选择一个整数
            line_y_list.append(random() * 100)

        #把每一条线的数据，加入x_y_list
        lines_list.append([line_x_list, line_y_list, choice(line_style_list), choice(color_list), line_name])

    # 绘制线形图
    mat_line(lines_list, 'CPU利用率', '时间', '百分比')