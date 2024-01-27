#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
# l1 = [1,2,3,4]
# l2 = ['a', 'b', 'c', 'd']
# a = list(zip(l1, l2))
# print(a)

dict1 = {1:'a', 2:'b', 3:'c', 4:'d'}
dict2 = dict1.get(4)
print(dict2)


#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sqlalchemy, asyncio, os, threading, re, hashlib
# 导入第七天的表Router，创建第9天的用于备份配置的表DeviceConfig, 并且外键关联到Router
from new_homework.day9.code.day9_1_creat_db import Router, DeviceConfig, engine
from new_homework.day7.code.ssh_client_netmiko import netmiko_show_cred
from new_homework.day9.code.smtp_send_mail_attachment import qyt_smtp_attachment
from new_homework.day9.code.diff_config import diff_txt

# 创建ORM会话，用于后续查询和写入数据库
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# 定义Netmiko 执行 show命令的协程函数
async def async_netmiko_show(task_id, ip, username, password, cmd):
    print(f'ID: {task_id} started')
    print(os.getpid(), threading.currentThread().ident)
    result = await loop.run_in_executor(None, netmiko_show_cred, ip, username, password, cmd)
    print(f'ID: {task_id} Stopped')
    # print(result)
    return result, ip
task_no = 1 # 循环任务计数号
tasks = [] # 协程的任务清单
# 从表Router， 得到所有路由器的IP地址和登录信息， 使用netmiko（协程）执行”show run“命令获取配置
for router in session.query(Router).all():
    # 产生协程任务
    task = loop.create_task(async_netmiko_show(task_no, router.ip, router.username,
                                               router.password, 'show run'))
    # 把产生的协程任务放入任务列表
    tasks.append(task)
    task_no += 1 # 任务号加1
    # session.add(tasks)
    # print(tasks)
    # session.commit()
# 完成全部协程任务
loop.run_until_complete(asyncio.wait(tasks))
# 获取全部协程结果
result_list = []
for i in tasks:
    result_list.append(i.result())
print(result_list)
# 每个结果是一个元组（配置，ip）
for device_config_raw, ip in result_list:
    # 获取hostname行，取其以下的内容。（教主洁癖的一个要求而已）
    split_result = re.split(r'\nhostname \S+\n', device_config_raw)
    device_config = device_config_raw.replace(split_result[0], '').strip()
    # 计算获取配置的MD5值
    m = hashlib.md5()
    m.update(device_config.encode())
    md5_value = m.hexdigest() # 返回结果是16进制的字符串
    # 通过IP地址找到后续对象，用于后续过滤
    device_obj = session.query(Router).filter_by(ip=ip).one()
    print(device_obj)
    print(ip)
    print(md5_value)
    #找到路由器最后一个备份（主键id + desc降序 + first()的DevicConfig对象
    last_config_bak = session.query(DeviceConfig).filter(DeviceConfig.router == device_obj).\
        order_by(sqlalchemy.desc(DeviceConfig.id)).first()
    print(last_config_bak)
    #比较MD5的值是否相同，如果不相同则发送邮件通知管理员
    if last_config_bak.config_md5 != 0: # md5_value:
        qyt_smtp_attachment('smtp.qq.com',
             '50840775',
             'bncduviqjaksbhab',
             '50840775@qq.com',
             '13811010442@139.com',
             f'设备：{ip}， 配置异常，其具体配置见正文:',
             diff_txt(last_config_bak.device_config, device_config)) # 使用diff比较的配置
      # 本次试验不管是否相同，都进行备份
    device_db_obj = DeviceConfig(router=device_obj, device_config=device_config,
                                     config_md5=md5_value)
    session.add(device_db_obj)
    session.commit()

