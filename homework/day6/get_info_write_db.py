#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

import sys

sys.path.extend(['/Python/automatic'])
from tools.snmpv2_getall_2023 import snmpv2_getall
from sqlalchemy.orm import sessionmaker
from create_sqlitedb import InternfaceMonitor, engine
from pprint import pprint

Session = sessionmaker(bind=engine)
session = Session()

ip_list = ['10.10.1.1', '10.10.1.2']


def get_info_writedb(ip_list, rocommunity):
    router_info_list = []
    for device_ip in ip_list:
        # 通过SNMP获取设备的所有信息, CPU, MEM和接口
        try:
            get_all = snmpv2_getall(device_ip, rocommunity)
            interfaces_list = get_all.get('interface_list')
            pprint(interfaces_list)
            # pprint(get_all)

            # {'cpu_usage': 1,
            #  'interface_list': [{'interface_in_bytes': 467927396,
            #                      'interface_name': 'GigabitEthernet1',
            #                      'interface_out_bytes': 109018913,
            #                      'interface_state': True},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'GigabitEthernet2',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': False},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'GigabitEthernet3',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': False},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'Null0',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': True}],
            #  'ip': '10.10.1.1',
            #  'mem_free': 1317816,
            #  'mem_usage': 66.77,
            #  'mem_use': 2647528}
            # {'cpu_usage': 16,
            #  'interface_list': [{'interface_in_bytes': 470041536,
            #                      'interface_name': 'GigabitEthernet1',
            #                      'interface_out_bytes': 106825323,
            #                      'interface_state': True},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'GigabitEthernet2',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': False},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'GigabitEthernet3',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': False},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'Null0',
            #                      'interface_out_bytes': 0,
            #                      'interface_state': True},
            #                     {'interface_in_bytes': 0,
            #                      'interface_name': 'Loopback0',
            #                      'interface_out_bytes': 23820,
            #                      'interface_state': True}],
            #  'ip': '10.10.1.2',
            #  'mem_free': 1405836,
            #  'mem_usage': 64.55,
            #  'mem_use': 2559508}
            # '''
            # 把CPU和内存信息构建对象(数据库记录)
            for interface in interfaces_list:
                interface_name = interface.get('interface_name')
                in_bytes = interface.get('interface_in_bytes')
                out_bytes = interface.get('interface_out_bytes')
                print(interface)

                if in_bytes and out_bytes:
                    interface_info = InternfaceMonitor(device_ip=device_ip,
                                                       interface_name=interface_name,
                                                       in_bytes=in_bytes,
                                                       out_bytes=out_bytes)

                    router_info_list.append(interface_info)
        except Exception as e:
            print(e)

    # pprint(router_info_list)

    session.add_all(router_info_list)
    session.commit()


if __name__ == '__main__':
    # ip地址与snmp community字符串
    get_info_writedb(ip_list, 'tcpip')
