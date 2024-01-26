#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from create_syslog_db import Syslog, engine
from sqlalchemy import func
from tools.matplotlib_Pie_Chart import mat_bing
from tools.test1 import qyt_smtp_img
import os
from jinja2 import Template


# 配置jinja2模板目录
tem_path = './templates/'

# jinja2读取邮件HTML模板
with open(tem_path + 'syslog_email.template',encoding='utf-8') as f:
    syslog_email_template = Template(f.read())


Session = sessionmaker(bind=engine)
session = Session()

# 严重级别名字列表
severity_level_name_list = []

# 严重级别数量列表
severity_level_count_list = []

# 数据库中找到严重级别名字, 严重级别数量的信息, 并写入列表
for level, count in session.query(Syslog.severity_level_name, func.count(Syslog.severity_level_name)).group_by(
        Syslog.severity_level_name).all():
    severity_level_name_list.append(level)
    severity_level_count_list.append(count)

# print(severity_level_name_list)
# print(severity_level_count_list)

# 发送SYSLOG设备的IP列表
device_ip_list = []

# 设备发送SYSLOG数量列表
device_log_count_list = []

# 数据库中找到发送SYSLOG设备的IP, 设备发送SYSLOG数量的信息, 并写入列表
for ip, count in session.query(Syslog.device_ip, func.count(Syslog.device_ip)).group_by(
        Syslog.device_ip).all():
    device_ip_list.append(ip)
    device_log_count_list.append(count)


# print(device_ip_list)
# print(device_log_count_list)

# 文件保存路径
current_dir = os.path.dirname(os.path.realpath(__file__))

# 保存严重级别分析图的文件名(没有扩展名)
severity_level_filename = 'severity_level'
# 保存主机分析图的文件名(没有扩展名)
device_ip_filename = 'device_ip'

# 拼接成为保存文件的绝对路径
save_file_severity_level_file = f'{current_dir}{os.sep}{severity_level_filename}.png'
save_file_device_ip_file = f'{current_dir}{os.sep}{device_ip_filename}.png'

# 使用饼状图呈现
mat_bing(severity_level_name_list, severity_level_count_list, 'SYSLOG严重级别分布图', save_file_severity_level_file)
mat_bing(device_ip_list, device_log_count_list, 'SYSLOG设备分布图', save_file_device_ip_file)

# 严重级别日志总数量
severity_total = sum(severity_level_count_list)

# 用于替换模板中的severity_level_count_html_list
severity_level_count_html_list = []
"""
<tbody class="text-center">
    {% for s in severity_level_count_html_list %}
        <tr>
            <td>{{ s.name }}</td><td>{{ s.log_count }}</td><td>{{ s.percent }}</td>
        </tr>
    {% endfor %}
</tbody>
"""
# 构建severity_level_count_html_list
for name, log_count in zip(severity_level_name_list, severity_level_count_list):
    severity_level_count_html_list.append({'name': name,
                                           'log_count': log_count,
                                           'percent': round((log_count / severity_total) * 100, 2)})

# 设备发送日志总数量
deice_log_total = sum(device_log_count_list)

# 用于替换模板中的device_ip_count_html_list
device_ip_count_html_list = []
"""
<tbody class="text-center">
    {% for d in device_ip_count_html_list %}
        <tr>
            <td>{{ d.ip }}</td><td>{{ d.log_count }}</td><td>{{ d.percent }}</td>
        </tr>
    {% endfor %}
</tbody>
"""
# 构建device_ip_count_html_list
for ip, log_count in zip(device_ip_list, device_log_count_list):
    device_ip_count_html_list.append({'ip': ip,
                                      'log_count': log_count,
                                      'percent': round((log_count / deice_log_total) * 100, 2)})

# 对jinja2模板进行替换, 产生邮件正文中的HTML部分
main_body_html = syslog_email_template.render(severity_level_count_html_list=severity_level_count_html_list,
                                              severity_level_filename=severity_level_filename,
                                              device_ip_count_html_list=device_ip_count_html_list,
                                              device_ip_filename=device_ip_filename)

    # 发送HTML邮件
qyt_smtp_img('smtp.qq.com',
             '58937909@qq.com',
             'la822ywq',
             '58937909@qq.com',
             '58937909@qq.com',
             '乾颐堂NetDevOps Syslog分析',
             main_body_html,
             [save_file_severity_level_file,
              save_file_device_ip_file])

# 删除产生的临时图片文件
if os.path.exists(save_file_severity_level_file):
    os.remove(save_file_severity_level_file)

if os.path.exists(save_file_device_ip_file):
    os.remove(save_file_device_ip_file)


# if __name__ == "__main__":
#     pass
