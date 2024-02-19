import pyshark  # pip3 install pyshark==0.4.5
from datetime import timezone, timedelta
from elasticsearch import Elasticsearch  # pip3 install elasticsearch==6.3.1

# 设置时区为UTC
tzutc_0 = timezone(timedelta(hours=0))

# 连接ElasticSearch
es = Elasticsearch("http://10.1.1.11:9200")

# PyShark读取PCAP数据包'pkt.pcap'
cap = pyshark.FileCapture('pkt.pcap', keep_packets=False)  # 读取pcap文件,数据包被读取后,不在内存中保存!节约内存!

i = 1


# 处理数据包的函数
def write_pkt_es(pkt):
    global i
    pkt_dict = {}
    # 使用Pyshark获取数据包中的所有字段
    for layer in pkt.__dict__.get('layers'):
        pkt_dict.update(layer.__dict__.get('_all_fields'))
    pkt_dict_final = {}
    # 把字段分割成为字典
    for key, value in pkt_dict.items():
        # 防止空键
        if key == '':
            continue
        else:
            # 替换键中的'.'到'_'
            pkt_dict_final[key.replace('.', '_')] = value

    # 格式为:2018-04-23T10:45:13.899Z. Note that we only have milliseconds and the T as separator and Z indicating UTC.
    # E的时间为UTC,所以需要切换时区
    pkt_dict_final.update({"sniff_time": pkt.sniff_time.astimezone(tzutc_0).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'})
    pkt_dict_final.update({'highest_layer': pkt.highest_layer})

    try:
        # 把ip_len转换到整数
        ip_len = int(pkt_dict_final.get('ip_len'))
        pkt_dict_final['ip_len'] = ip_len

        # 添加数据到索引
        # 索引ID为1
        # doc_type类型为doc
        # body为准备好的包含数据包信息的字典
        resp = es.index(index="qyt-pyshark-index", id=i, doc_type='doc', body=pkt_dict_final)
        print(resp['result'])

        i += 1

    except Exception:
        pass


# 把函数应用到数据包
cap.apply_on_packets(write_pkt_es)
