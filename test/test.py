ips = ['10.10.1.1', '10.10.1.2']


def get_info_wrdb(ips, rocommunity):
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
                                            mem_use=mem_use,
                                            mem_free=mem_free)
        router_ip_list.append(router_usage_record)
        print(router_ip_list)