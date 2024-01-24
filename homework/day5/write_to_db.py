#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import sys

sys.path.extend(['/Python/protocol2022/'])
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

client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, influx_db)
while True:
    # ----------------------写入CPU 内存数据------------------------
    for ip in router_ip:
        getall_result = snmpv2_getall(ip, snmp_community)
        current_time = datetime.datetime.utcnow().isoformat("T")
        cpu_mem_body = [
            {
                "measurement": "router_monitor",
                "time": current_time,
                "tags": {
                    "device_ip": getall_result.get('ip'),
                    "device_type": "IOS-XE"
                },
                "fields": {
                    "cpu_usage": getall_result.get('cpu_usage'),
                    "mem_usage": getall_result.get('mem_usage'),

                },
            }
        ]
        print(cpu_mem_body)
        client.write_points(cpu_mem_body)
if __name__ == "__main__":
    pass
