#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket
import sys
import struct
import hashlib
import pickle

#windows 运行
address = ('0.0.0.0', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP服务器就绪！等待客户数据!')
while True:
    try:
        # 接收数据[限制发送大小为512]
        recv_source_data = s.recvfrom(512)

        rdata,addr = recv_source_data

        version = rdata [:2]

        pkt_type = rdata [2:4]
        # print(pkt_type)
        seq_id = rdata [4:8]
        # print(seq_id)
        len_ = rdata [8:16]
        # print(len_)
        header = rdata [:16]
        # print(header)
        data_and_hash = rdata [16:]
        # print(data_and_hash)
        recv_data = rdata [16:-16]
        # print(recv_data)
        hash_value = data_and_hash[-16:]

        version_unpack = struct.unpack('>H', version)
        # print(version_unpack)
        pkt_type_unpack = struct.unpack('>H', pkt_type)
        # print(pkt_type_unpack)
        seq_id_unpack = struct.unpack('>I', seq_id)
        # print(seq_id_unpack)
        len_unpack = struct.unpack('>Q', len_)
        # print(len_unpack)

        recv_data_unpack = pickle.loads(recv_data)
        # print('数据：',recv_data_unpack)
        m = hashlib.md5()
        m.update(header + recv_data)
        md5_value = m.digest()

        if hash_value == md5_value:
            print('-' * 80)
            print("{0:<30}:{1:<30}".format("数据源自于", str(addr)))
            print("{0:<30}:{1:<30}".format("数据序列号", seq_id_unpack[0]))
            print("{0:<30}:{1:<30}".format("数据长度为", len_unpack[0]))
            print("{0:<30}:{1:<30}".format("数据内容为", str(recv_data_unpack)))
        else:
            print('MD5校验错误')
    except KeyboardInterrupt:
        sys.exit()

