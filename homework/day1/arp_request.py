#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import logging

from homework.day1.time_decorator import run_time

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *

import ipaddress
from multiprocessing.pool import ThreadPool


def arp_request(ip):
    try:
        arp_pkt = ARP(pdst=ip)
        arp_req = sr1(arp_pkt, verbose=False, timeout=1)
        return ip, arp_req.getlayer('ARP').fields.get('hwsrc')  # 返回IP，MAC
    except AttributeError:
        return ip, None


@run_time()
def arp_scan_thread(network):
    pool = ThreadPool(100)  # 多线程
    net = ipaddress.ip_network(network)
    arp_scan = {}
    results = [pool.apply_async(arp_request, args=(str(ip),)) for ip in net]  # args=(str(ip),) 元组
    pool.close()
    pool.join()

    for i in results:
        if i.get()[1]:
            arp_scan[i.get()[0]] = i.get()[1]
    # print(arp_scan)
    return arp_scan


if __name__ == "__main__":
    for ip, mac in arp_scan_thread('10.10.1.0/30').items():
        print(f'IP地址:{ip},MAC地址:{mac}')
