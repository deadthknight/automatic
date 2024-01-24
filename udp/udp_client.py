#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket

address = ('10.10.1.100', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input('请输入数据：')
    # 数据输入为空，发送空数据，退出
    if not msg:
        #  msg.encode 将字符串消息 msg 编码为字节流。在网络传输中，通常需要将文本数据编码为字节数据，而encode() 方法执行这个操作。
        s.sendto(msg.encode(), address)
        break
    # 数据不为空，发送数据
    s.sendto(msg.encode(), address)
s.close()
if __name__ == "__main__":
    pass
