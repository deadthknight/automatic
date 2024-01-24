#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from sqlalchemy.orm import sessionmaker
from create_db_row import RouterMonitor, engine
from get_wr_db import ip_list
from matplotlib_linear import mat_line
from random import choice
from pprint import pprint
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()

# 过滤一个小时以内的数据
now = datetime.now()
one_hours_before = now - timedelta(hours=1)
# print(one_hours_before)

# 线的颜色列表, 随机选择
color_list = ['red', 'blue', 'green', 'yellow']

# 线的类型列表, 随机选择
line_style_list = ["solid", "dashed"]

# 最终绘图用的CPU列表
cpu_line_list = []

# 最终绘图用的内存列表
mem_line_list = []

i = 0

for ip in ip_list:
    # 过滤特定IP(设备), 一个小时内的数据库记录
    router_infos = session.query(RouterMonitor).filter(RouterMonitor.record_datetime >= one_hours_before,
                                                       RouterMonitor.device_ip == ip
                                                       )

    # 这个设备记录时间列表
    time_list = []
    # 这个设备记录的CPU利用率的列表
    cpu_list = []
    # 这个设备记录的内存利用率的列表
    mem_list = []

    # 分析这个设备的每一个记录
    for router_info in router_infos:
        # 写入时间记录
        time_list.append(router_info.record_datetime)
        # 写入CPU利用率记录
        cpu_list.append(router_info.cpu_useage_percent)
        # 计算并写入内存利用率记录
        mem_use = router_info.mem_use
        mem_free = router_info.mem_free
        mem_percent = round((mem_use / (mem_free + mem_use)) * 100, 2)
        mem_list.append(mem_percent)

    # 写入到最终绘图用的CPU列表
    cpu_line_list.append([time_list, cpu_list, choice(line_style_list), color_list[i], ip])
    # 写入到最终绘图用的内存列表
    mem_line_list.append([time_list, mem_list, choice(line_style_list), color_list[i], ip])

    # i用来计数, 选择颜色
    i += 1

# 打印数据点
pprint(cpu_line_list)
pprint(mem_line_list)

# 绘制线形图
mat_line(cpu_line_list, 'CPU利用率', '记录时间', '百分比')
mat_line(mem_line_list, 'MEM利用率', '记录时间', '百分比')
