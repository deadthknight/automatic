#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient

influx_host = '10.10.1.200'
router_ip = ['10.10.1.1', '10.10.1.2']
snmp_community = "tcpip"
influx_db = "qytdb"
influx_port = 8086
influx_measurement = "router_monitor"
influx_admin = "admin"
influx_user = "qytdbuser"
influx_password = "Cisc0123"

if __name__ == '__main__':
    client = InfluxDBClient(influx_host, influx_port, influx_admin, influx_password)

    # 查看数据库
    print(client.get_list_database())
    # 创建数据库
    print(client.create_database('testdb'))
    print(client.get_list_database())
    # 删除数据库
    print(client.drop_database('testdb'))
    print(client.get_list_database())

    client = InfluxDBClient(influx_host, 8086, influx_user, influx_password, influx_db)
    measurements_result = client.query('show measurements;')  # 显示数据库中的表
    print(f"Result: {format(measurements_result)}")

    retention_result = client.query('show retention policies on "qytdb";')  # 显示数据库中的表
    print(f"Result: {format(retention_result)}")



