#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket
import sys
# UDP套接字在所有可用网络接口上监听端口号6666
address = ('0.0.0.0', 6666)
# 创建UDP套接字Socket, AF_INET为IPv4, SOCK_DGRAM为Datagram就是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 套接字绑定到地址,元组(host, port)
s.bind(address)

print('等待客户端发送数据！')
while True:
    try:
        #可接受数据的大小
        data_addr = s.recvfrom(512)
        print(data_addr)
        data, addr = data_addr
        if not data:
            print('数据为None')
            break
        #  系统默认decode 用utf-8 解码
        print('数据为:', data.decode(), '发送地址为：', addr)

    except KeyboardInterrupt:
        sys.exit()

