#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket
import struct

import hashlib
import pickle

def udp_send_date(ip,port,data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1
    for x in data_list:

        send_date = pickle.dumps(x)
        ver_encode =struct.pack('>H',version)
        pkt_type_enconde =struct.pack('>H',pkt_type)
        seq_id_enconde = struct.pack('>I',seq_id)
        # len_total = 8 + len(send_date) + 16
        len_encode = struct.pack('>Q',len(send_date))
        md5 = hashlib.md5()
        md5.update(send_date)
        date_md5 = md5.hexdigest()
        pkt = ver_encode + pkt_type_enconde + seq_id_enconde +len_encode + send_date + date_md5

        s.sendto(pkt,address)
        seq_id+=1
    s.close()
if __name__ == "__main__":
    from datetime import datetime

    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}, {'datetime': datetime.now()}]
    udp_send_date('10.10.1.100', 6666, user_data)
