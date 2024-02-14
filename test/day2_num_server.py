#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket
import sys
import struct
import hashlib
import  pickle

address = ('0.0.0.0',6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print ('UDP 服务器就绪！等待客户数据！')

while True:
    try:
        recv_source_data =s.recvfrom(512)

        rdata,addr = recv_source_data

        # rdata_header = struct.unpack('>HHIQ', rdata[:16])

        seq_id = struct.unpack('>I',rdata[4:8])
        # print(seq_id)

        len_unpack = struct.unpack('>Q',rdata[8:16])

        date_rcv = rdata[16:-16]

        date_unpack = pickle.loads(date_rcv)

        hash_rcv = rdata[-16:]

        md5 = hashlib.md5()

        md5.update(date_rcv)

        date_md5 = md5.digest()

        # date_md5 = date_md5.encode()
        if date_md5 == hash_rcv:
            print('-' * 80)
            print("{0:<30}:{1:<30}".format("数据源自于", str(addr)))
            print("{0:<30}:{1:<30}".format("数据序列号", seq_id[0]))
            print("{0:<30}:{1:<30}".format("数据长度为", len_unpack[0]))
            print("{0:<30}:{1:<30}".format("数据内容为", str(date_unpack)))
        else:
            print('MD5校验错误')
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    pass
