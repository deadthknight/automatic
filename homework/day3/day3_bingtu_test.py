#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

# import matplotlib
# matplotlib.use('agg')  # 或者使用 'Qt5Agg'


from matplotlib import pyplot as plt


def mat_bing(name_list, count_list, bing_name):
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.figure(figsize=(6, 6))

    patches, l_text, p_text = plt.pie(count_list,
                                      labels=name_list,
                                      labeldistance=1.1,
                                      autopct='%3.1f%%',
                                      shadow=False,
                                      startangle=90,
                                      pctdistance=0.6)

    for t in l_text:
        t.set_size = 30

    for t in p_text:
        t.set_size = 30

    plt.axis('equal')
    plt.title(bing_name)
    plt.legend()

    # plt.savefig('figure.png')
    plt.show()


if __name__ == "__main__":
    mat_bing(['名称1', '名称2', '名称3'], [1000, 123, 444], '测试饼图')
    # import os
    # print(os.getcwd())
    # print(open('figure.png'))
