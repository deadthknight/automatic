#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, BigInteger
import datetime
import os

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))  # 设置时区为东八区

# os.path.dirname(os.path.realpath(__file__) 当前文件目录

# os.path.sep 是 Python 中用于获取路径分隔符的常量。这个值表示文件路径中的目录分隔符，它取决于运行 Python 的操作系统。
# 在 Windows 上为反斜杠 \（例如：C:\Users\Username\Documents）
# 在 Unix/Linux 上为正斜杠 /（例如：/home/username/documents
# 固定数据库文件位置, 与当前文件相同目录
db_file_name = f'{os.path.dirname(os.path.realpath(__file__))}{os.path.sep}sqlalchemy_syslog_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Base = declarative_base()


# 记录路由器接口信息数据库表
class InternfaceMonitor(Base):
    __tablename__ = 'interface_monitor'

    id = Column(Integer, primary_key=True)  # 唯一ID, 主键
    device_ip = Column(String(64), nullable=False)  # 设备IP地址
    interface_name = Column(String(64), nullable=False)  # 接口名称
    in_bytes = Column(BigInteger, nullable=False)  # 入向字节数
    out_bytes = Column(BigInteger, nullable=False)  # 出向字节数

    # 记录时间
    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(路由器IP: {self.device_ip} " \
               f"| 时间: {self.record_datetime} " \
               f"| 接口名称: {self.interface_name} " \
               f"| 入向字节数: {self.in_bytes} " \
               f"| 出向字节数: {self.out_bytes})"


if __name__ == '__main__':
    # 如果存在老数据库文件就删除
    if os.path.exists(db_file_name):
        os.remove(db_file_name)

    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)


