#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Frank

from pissh import PiSSH



host = '169.254.217.14'    #设置为机箱IP
username = 'sshuser'
password = '123456'         #需要开启机箱的SSH功能，
port = 22


pi =PiSSH(host=host,port=port,username=username,password=password,timeout=1)  #实例化
pi.read_recv_time_delay =0.05                    #设置回读延时，若回读不完整可以调大，目前默认0.05秒，我在我的电脑上测试没问题，默认就是0.05s

if __name__ == '__main__':

    while True:
        command = input('请输入指令》》').strip().upper()
        if command == 'Q':
            break    #按q退出
        res = pi.send(command)
        print(res)





