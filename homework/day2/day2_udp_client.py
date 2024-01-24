#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import socket
import struct
import hashlib
import pickle


def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1

    for x in data_list:
        send_data = pickle.dumps(x)
        version_pack = struct.pack('!H', version)
        pkt_pack = struct.pack('!H', pkt_type)
        seq_id_pack = struct.pack('!I', seq_id)
        len_pack = struct.pack('!Q', len(send_data))

        header_pack = version_pack + pkt_pack + seq_id_pack + len_pack

        checksum = hashlib.md5()
        checksum.update(header_pack + send_data)
        hash_value = checksum.digest()
        s.sendto(header_pack + send_data + hash_value, address)
        seq_id += 1
    s.close()


if __name__ == "__main__":
    from datetime import datetime

    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}, {'datetime': datetime.now()}]
    udp_send_data('10.10.1.100', 6666, user_data)
