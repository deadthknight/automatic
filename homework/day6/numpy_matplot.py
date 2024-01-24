#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from create_sqlitedb import InternfaceMonitor, engine
import numpy as np
from matplotlib_linear import mat_line
from pprint import pprint
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()

# 过滤一个小时以内的数据
now = datetime.now()
one_hours_before = now - timedelta(hours=1)

# 线的颜色列表，随机选择
color_list = ['red', 'blue', 'green', 'yellow']

# 线的类型列表，随机选择
line_style_list = ['solid', 'dashed']

# 找到唯一的device_ip 和 interface_name 的组合
router_if_infos = session.query(InternfaceMonitor.device_ip,
                                InternfaceMonitor.interface_name).group_by \
    (InternfaceMonitor.device_ip, InternfaceMonitor.interface_name).all()

# print(router_if_infos)
# [('10.10.1.1', 'GigabitEthernet1'), ('10.10.1.2', 'GigabitEthernet1')]

# 入向接口速率
in_speed_lines_list = []

# 出向接口速率
out_speed_lines_list = []

# 对循环进行计较
count = 0

for device_ip, interface_name in router_if_infos:
    # 过滤最近一个小时，特定device_ip与interface_name组合的全部记录数据
    device_if_info = session.query(InternfaceMonitor). \
        filter(InternfaceMonitor.device_ip == device_ip,
               InternfaceMonitor.interface_name == interface_name). \
        filter(InternfaceMonitor.record_datetime >= one_hours_before).all()
    # pprint(device_if_info)
    # 保存入向字节数的列表
    in_bytes_list = []
    # 保存出向字节数的列表
    out_bytes_list = []
    # 保存记录时间的列表
    record_time_list = []

    # 从过滤出来的数据库条目中，提取数据并添加到3个列表中
    for device_if in device_if_info:
        in_bytes_list.append(device_if.in_bytes)
        out_bytes_list.append(device_if.out_bytes)
        record_time_list.append(device_if.record_datetime)

    # print(in_bytes_list)
    # print(out_bytes_list)
    # print(record_time_list)

# ---------------使用Numpy计算字节的增量------------------
# numpy的diff计算列表的差值
# np.diff([x for x in range (5)])
# The differences between adjacent elements [1-0, 2-1, 3-2, 4-3] result in the array [1, 1, 1, 1]
# 通过这种方式获取两次获取的字节数的差值

    diff_in_bytes_list = list(np.diff(in_bytes_list))
    diff_out_bytes_list = list(np.diff(out_bytes_list))
    print(diff_in_bytes_list)
# ---------------使用Numpy计算时间的增量（秒）------------------
# 计算两次时间对象的秒数的差值
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]
    print(diff_record_time_list)

# ---------------------计算入方向和出方向的速率------------------
# 计算速率
# * 8 得到bit数
# /1000 计算kb
# / x[1] 计算kbps
# round(x, 2) 保留两位小数
# zip把字节差列表 和时间差列表压到一起
    in_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                             zip(diff_in_bytes_list, diff_record_time_list)))
    out_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                              zip(diff_out_bytes_list, diff_record_time_list)))
    print(in_speed_list)
# 切掉第一个时间记录点，剩下为速率的记录时间
#     print(record_time_list)
    record_time_list = record_time_list[1:]
    # print(record_time_list)
# 开始数据清洗
    clean_record_time_list = []
    clean_in_speed_list = []
    clean_out_speed_list = []

    for r, i, o in zip(record_time_list, in_speed_list, out_speed_list):
        if i > 0 and o > 0:  # 如果入向和出向速率都大于0，写入清洗后的数据
            clean_record_time_list.append(r)
            clean_in_speed_list.append(i)
            clean_out_speed_list.append(o)

# print(clean_record_time_list)
# print(clean_in_speed_list)
# print(out_speed_list)

# 写入数据到lines_list
    in_speed_lines_list.append([clean_record_time_list,
                                clean_in_speed_list,
                                line_style_list[count],
                                color_list[count],
                                f'RX:{device_ip}:{interface_name}'])
    out_speed_lines_list.append([clean_record_time_list,
                                 clean_out_speed_list,
                                 line_style_list[count],
                                 color_list[count],
                                 f'RX:{device_ip}:{interface_name}'])
    count +=1

# 绘制线形图
# pprint(in_speed_lines_list)
mat_line(in_speed_lines_list, '入向速率', '记录时间', 'kbps')
mat_line(out_speed_lines_list, '出向速率', '记录时间', 'kbps')

