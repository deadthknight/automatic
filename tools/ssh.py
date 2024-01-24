#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import paramiko


def device_ssh(ip, username, password, port=22, cmd=''):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, port=port)
        ssh.exec_command(cmd)  # executes command
        stdin, stdout, stderr = ssh.exec_command(cmd)
        return stdout.read().decode()
    except Exception as error:
        return f'Error:{error}'


if __name__ == "__main__":
    print(device_ssh(ip='10.10.1.1', username='admin', password='admin', cmd='ping 10.10.1.2 repeat 1 size 1000 '))
# device_ssh(ip='10.10.1.2', username='admin', password='admin', cmd='ping 10.10.1.1 repeat 20 ')
# print ('ok')
