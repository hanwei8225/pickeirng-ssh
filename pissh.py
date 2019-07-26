#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Frank

import paramiko,time



class PiSSH():
    def __init__(self,host:str='',port:int = 22,username:str = '',password:str = '',timeout:float =1.0):
        '''

        :param host:
        :param port:
        :param username:
        :param password:
        :param timeout: 该参数是连接ssh时的超时设置，单位为秒
        '''
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout               #该参数是连接ssh时的超时设置，单位为秒
        self.channel = None
        self.ssh_client = None
        self.read_recv_time_delay = 0.05      #发送指令后回读的延时，若send函数的回读值不完整适当调大该参数，单位是秒


    def __new__(cls, *args, **kwargs):
        '''
        单例模式，保证只有一个连接
        :param args:
        :param kwargs:
        :return:
        '''
        if not hasattr(PiSSH,'_instance'):
            cls._instance = super(PiSSH, cls).__new__(cls)
        return cls._instance




    def _connect(self):
        '''
        连接sshhost，并且开启一个shell的channel，用于信息的收发，相当于直接在远程机上打开shell，
        一般在实例化对象之后，只要不销毁，就只会连接一次，若连接超时或者突然断开连接会抛出异常
        :return:
        '''
        if not self._connected():

            self.ssh_client = paramiko.SSHClient()

            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.ssh_client.connect(hostname = self.host,
                                    port = self.port,
                                    username= self.username,
                                    password = self.password,
                                    timeout = self.timeout
                                    )
            self.channel = self.ssh_client.invoke_shell()



    def _connected(self):
        '''
        检测是否已连接
        :return:
        '''
        if self.channel and self.ssh_client.get_transport():
            if self.ssh_client.get_transport().is_active():
                return True
            else:
                return False
        return False


    def send(self,command:str) -> str:
        '''
        发送指令，返回指令执行结果的字符串
        :param command:
        :return:
        '''
        self._connect()
        self.channel.send(command+'\n')
        time.sleep(self.read_recv_time_delay)
        result =''
        while self.channel.recv_ready():
            result += self.channel.recv(1024).decode('utf-8')

        return result


    def __del__(self):
        '''
        销毁的时候自动关闭连接
        :return:
        '''
        if self._connected():
            self.channel.close()
            self.ssh_client.close()
