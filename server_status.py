# -*- coding: utf-8 -*-
from unit import unit_reqests
import os
import socket


class server_status():
    '''
    服务器状态及项目入口
    '''
    def __init__(self):
        self.varsion = '1.0.0'
        self.url_status_server = 'http://oa.9oe.com/index.php/book/apiserver/index/'
        self.url_status_server_test = 'http://www.123.com/index.php/book/apiserver/index/'
        self.server_info_name = ''
        self.server_info_macaddress = ''
        self.server_info_system = ''

    def server_test(self):
        '''
        测试与服务器的通讯
        :return:
        '''
        httpGet = unit_reqests.getHtmlData(self.url_status_server_test, dubeg=True)
        print(httpGet)

    def update_status(self):
        '''
        更新状态
        :return:
        '''
        data = {
            'model': 'upstat_status_server',
            'server_info_name': self.get_info_name(),
        }
        httpGet = unit_reqests.postHtmlData(self.url_status_server_test, data=data, dubeg=True)
        print(httpGet)

    def get_info_name(self):
        try:
            self.server_info_name = socket.gethostname()
        except:
            self.server_info_name = 'test'
        return self.server_info_name


if __name__ == '__main__':
    # server_status().server_test()

    server_status().update_status()
