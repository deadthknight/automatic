#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-


# import matplotlib
#
# matplotlib.use('agg')  # linux

from matplotlib import pyplot as plt


def mat_bing(name_list, count_list, bing_name):

    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.figure(figsize=(7, 7))

    patches, l_text, p_text = plt.pie(count_list,
                                      labels=name_list,
                                      labeldistance=1.1,
                                      autopct='%3.1f%%',
                                      shadow=False,
                                      startangle=90,
                                      pctdistance=0.6)
#   labeldistance='' 标签离圆心的距离
#   autopct = '%3.1f%%' 表示显示每个部分的百分比，格式为带有一位小数的浮点数，占据3个字符的位置，然后跟着百分号。
#   pctdistance = 0.6表示将百分比标签放置到半径的0.6倍远的位置

    for t in l_text:
        t.set_size = 30

    for t in p_text:
        t.set_size = 30

    plt.axis('equal')   # x 轴和 y 轴的单位长度相等
    plt.title(bing_name)
    plt.legend(loc='lower right')
    '''
    图例位置
    'upper right': 右上角
    'upper left': 左上角
    'lower left': 左下角
    'lower right': 右下角
    'right': 右侧
    'center left': 左中
    'center right': 右中
    'lower center': 下中
    'upper center': 上中
    'center': 中心
    '''

    # plt.savefig('figure_homework.png')
    plt.show()

if __name__ == "__main__":
    import re
    from tools.ssh import device_ssh
    netflow_info = device_ssh(ip='10.10.1.1', username='admin', password='admin',
                              cmd='sh flow monitor name qytang-monitor cache format table')
    # print(netflow_info)
    pattern = re.compile(r'(port ssh|port telnet|layer7 ping)\s+(\d+)')
    # print(pattern.match)
    netflow_info_re = re.findall(pattern, netflow_info)
    print(netflow_info_re)
    name_list = []
    count_list = []
    for line in netflow_info.strip().split("\n"):
        result = pattern.match(line)
        if result:
            name_list.append(result.groups()[0])
            count_list.append(result.groups()[1])

    mat_bing(name_list, count_list, '第三条作业Netflow')

