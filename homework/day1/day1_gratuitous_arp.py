#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *
from tools.get_mac_netifaces import get_mac_address
from tools.scapy_iface import scapy_iface


def gratuitous_arp(ip_address, ifname):
    localmac = get_mac_address(ifname)
    print(localmac)
    gratuitous_arp_pkt = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff') / ARP(op=2, hwsrc=localmac, hwdst=localmac,
                                                                            psrc=ip_address, pdst=ip_address)
    sendp(gratuitous_arp_pkt, iface=scapy_iface(ifname), verbose=False)


if __name__ == "__main__":

    while True:
        gratuitous_arp('10.10.1.1', ifname='ens224')
        time.sleep(1)

#