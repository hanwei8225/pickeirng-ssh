#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Frank

import paramiko,time

host = '169.254.217.14'
username = 'sshuser'
password = '123456'
port = 22


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect(hostname=host,port=port,username=username,password=password,timeout=1)

# stdin,stdout,stderr  = ssh.exec_command('',get_pty=True)
# stdin.write('HELP\r\n')
# time.sleep(0.01)
# stdout.channel.close()
# print(stdout.read().decode('utf-8'))
# ssh.close()

print(ssh.get_transport().is_active())
channel = ssh.invoke_shell()
channel.send('HELP\n')
time.sleep(0.08)

res = channel.recv(5280)

print(res.decode('utf-8'))
print('*************************************************')
channel.send('COA\n')
time.sleep(0.08)

res = channel.recv(1024)
# err = channel.recv_stderr(1024)
print(res.decode('utf-8'))
# print('-----',err.decode('utf-8'))
channel.close()
ssh.close()


















# host = '192.168.56.101'
# host ='101.132.237.189'
# username='root'
# password='hanwei-8225'

