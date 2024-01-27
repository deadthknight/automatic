#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, files=None):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    tos = to_mail.split(';')  # 把多个邮件接受者通过';'分开
    date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    msg["Subject"] = subj  # 主题
    msg["From"] = from_mail  # 发件人
    msg["To"] = to_mail  # 收件人
    msg["Date"] = date  # 发件日期

    # 邮件正文为Text类型, 使用MIMEText添加
    # MIME类型介绍 https://docs.python.org/2/library/email.mime.html
    part = MIMEText(main_body)
    msg.attach(part)  # 添加正文

    if files:  # 如果存在附件文件
        for file in files:  # 逐个读取文件,并添加到附件
            # MIMEXXX决定了什么类型 MIMEApplication为二进制文件
            # 添加二进制文件
            part = MIMEApplication(open(file, 'rb').read())
            # 添加头部信息, 说明此文件为附件,并且添加文件名
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            # 把这个部分内容添加到MIMEMultipart()中
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)  # 连接邮件服务器
    server.login(username, password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(from_mail, tos, msg.as_string())  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('邮件已经成功发出！')  # 如果没有故障发生，打印'邮件已经成功发出！'！


if __name__ == '__main__':
    pass



