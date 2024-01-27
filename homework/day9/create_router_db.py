#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# 使用正则表达式切分配置, 获取hostname行, 及其以下的内容(教主洁癖的一个要求而已)
import re

# 用于计算设备配置的MD5值
import hashlib

# 导入第七天的表Router
# 创建了第九天的用于备份配置的表DeviceConfig, 并且外键关联到Router
from homework.day7.create_db import Router, DeviceConfig, engine

# 后续的降序查询会被用到
import sqlalchemy

# netmiko show 函数, 与正课项目中的netmiko代码略有区别, 返回(show结果, host)
from tools.ssh_clinet_netmiko import netmiko_show_cred

# 正课项目中发送邮件的代码
from tools_project.smtp_send_mail_attachment import qyt_smtp_attachment

# 正课项目中较文本的代码
from tools_project.diff_config import diff_txt

# 协程相关
import asyncio
import os
import threading

# 创建ORM会话, 用于后续查询和写入数据库
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# 定义Netmiko执行show命令的携程函数
async def async_netmiko_show(task_id, ip, username, password, cmd):
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.currentThread().ident)
    result = await loop.run_in_executor(None, netmiko_show_cred, ip, username, password, cmd)
    print(f'ID: {task_id} Stopped')
    return result

# 循环任务计数号
task_no = 1

# 协程的任务清单
tasks = []

# 从表Router, 得到所有路由器的IP地址和登录信息, 使用netmiko(协程)执行"show run"命令获取配置
for router in session.query(Router).all():
    # 产生协程任务
    task = loop.create_task(async_netmiko_show(task_no,
                                               router.ip,
                                               router.username,
                                               router.password,
                                               "show run"))
    # 把产生的携程任务放入任务列表
    tasks.append(task)
    # 任务号加1
    task_no += 1

# 完成全部协程任务
loop.run_until_complete(asyncio.wait(tasks))

# 获取全部携程任务的结果
result_list = []

for i in tasks:
    result_list.append(i.result())

# 每一个结果是一个元祖(配置, ip)
for device_config_raw, ip in result_list:
    # 获取hostname行, 及其以下的内容(教主洁癖的一个要求而已)
    split_result = re.split(r'\nhostname \S+\n', device_config_raw)
    device_config = device_config_raw.replace(split_result[0], '').strip()

    # 计算获取配置的MD5值
    m = hashlib.md5()
    m.update(device_config.encode())
    md5_value = m.hexdigest()  # 返回结果是16进制的字符串

    # 通过IP地址找到Router对象, 用于后续过滤
    device_obj = session.query(Router).filter_by(ip=ip).one()

    # 找到这个路由器, 最后一次备份(主键id + desc降序 + fisrt())的DeviceConfig对象
    last_config_bak = session.query(DeviceConfig).\
        filter(DeviceConfig.router == device_obj).\
        order_by(sqlalchemy.desc(DeviceConfig.id)).first()

    # 比较MD5值是否相同, 如果不相同就发送邮件通知管理员
    if last_config_bak and last_config_bak.config_md5 != md5_value:
        qyt_smtp_attachment('smtp.qq.com',
                            '58937909@qq.com',
                            'dgoplovftflqbgjd',
                            '58937909@qq.com',
                            '58937909@qq.com',
                            f'设备:{ip}, 配置异常, 具体配置看正文:',
                            diff_txt(last_config_bak.device_config, device_config)  # 使用diff比较的配置
                            )

    # 本次实验不管是否相同, 都进行备份
    device_db_obj = DeviceConfig(router=device_obj,
                                 device_config=device_config,
                                 config_md5=md5_value)
    session.add(device_db_obj)
    session.commit()

