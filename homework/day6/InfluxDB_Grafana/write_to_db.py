#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import sys

sys.path.extend(['/Python/automatic/'])
from tools.snmpv2_getall_2023 import snmpv2_getall
import datetime
from influxdb import InfluxDBClient
from connect_to_db import (influx_host,
                           router_ip,
                           snmp_community,
                           influx_db,
                           influx_port,
                           influx_user,
                           influx_password)
from pprint import pprint

client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, influx_db)
router_interface_in_out = []
    # ----------------------写入CPU 内存数据------------------------
for ip in router_ip:
    getall_result = snmpv2_getall(ip, snmp_community)
    # print(getall_result)
    interfaces_list = getall_result.get('interface_list')
    current_time = datetime.datetime.utcnow().isoformat("T")
    for interface in interfaces_list:
        interface_name = interface.get('interface_name')
        in_bytes = interface.get('interface_in_bytes')
        out_bytes = interface.get('interface_out_bytes')
        # print(interface)
        if in_bytes and out_bytes:
            interface_in_out_body = {"measurement": "router_monitor",
                                     "time": current_time,
                                     "tags": {"device_ip": getall_result.get('ip'),
                                              "interface_name": interface_name},
                                     "fields": {"in_bytes": in_bytes,"out_bytes": out_bytes},}
            # print(interface_in_out_body)
            router_interface_in_out.append(interface_in_out_body)
# pprint(router_interface_in_out)
client.write_points(router_interface_in_out)
if __name__ == "__main__":
    pass
