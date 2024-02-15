#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from pprint import pprint
import sys
sys.path.extend(['/Python/automatic'])
from tools.snmpv2_getall_2023 import snmpv2_getall
from sqlalchemy.orm import sessionmaker
from create_db_row import RouterMonitor, engine


Session = sessionmaker(bind=engine)
session = Session()

ip_list = ['10.10.1.1', '10.10.1.2']


def get_info_writedb(ip_list , rocommunity):
    router_info_list = []
    for ip in ip_list:
        # 通过SNMP获取设备的所有信息, CPU, MEM和接口
        try:
            get_all = snmpv2_getall(ip, rocommunity)
            # pprint(get_all)

            # 把CPU和内存信息构建对象(数据库记录)
            router_info = RouterMonitor(device_ip=get_all.get('ip'),
                                        cpu_useage_percent=get_all.get('cpu_usage'),
                                        memory_usage=get_all.get('mem_usage'),
                                        mem_use=get_all.get('mem_use'),
                                        mem_free=get_all.get('mem_free')
                                        )
            router_info_list.append(router_info)
            # pprint(router_info_list)
        except Exception:
            pass
    session.add_all(router_info_list)
    session.commit()


if __name__ == '__main__':
    # ip地址与snmp community字符串
    get_info_writedb(ip_list, 'tcpip')


