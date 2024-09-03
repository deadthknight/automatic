#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import sys

sys.path.extend(['/Python/automatic/'])
from sqlalchemy.orm import sessionmaker
from create_db_row import RouterMonitor, engine
from tools.snmpv2_getall_2023 import snmpv2_getall

Session = sessionmaker(bind=engine)
session = Session()

ips = ['10.10.1.1', '10.10.1.2']
def get_info_wrdb(ips,rocommunity='tcpip'):
    router_ip_list = []
    for ip in ips:
        get_all = snmpv2_getall(ip, rocommunity)
        cpu_usage = get_all.get('cpu_usage')
        mem_usage = get_all.get('mem_usage')
        mem_use = get_all.get('mem_use')
        mem_free = get_all.get('mem_free')
        router_usage_record = RouterMonitor(device_ip=ip,
                                            cpu_useage_percent=cpu_usage,
                                            memory_usage=mem_usage,
                                            # mem_use=None,
                                            # mem_free=None
                                            )
        router_ip_list.append(router_usage_record)
        print(router_ip_list)
    session.add_all(router_ip_list)
    session.commit()


if __name__ == "__main__":
    ips = ['10.10.1.1', '10.10.1.2']
    get_info_wrdb(ips)
    pass

