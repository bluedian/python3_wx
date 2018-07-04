# -*- coding: utf-8 -*-
from unit import unit_reqests
from bs4 import BeautifulSoup


class wx_account():
    def __init__(self):
        self.varsion = '1.0.1'
        self.wx_account = ''
        self.wx_account_name = ''
        self.wx_account_authname = ''
        self.wx_account_memo = ''
        self.server_address = 'http://www.123.com/index.php/wx/'

    def getServerWxAccount(self):
        mod = 'apiaccount/'
        data = {
            'model': 'get_wx_account',
        }
        url_server_all = self.server_address + mod
        html = unit_reqests.postHtmlData(url_server_all, data=data)
        return html

    def getUrlWxSogou(self, account_name=None, account_login=None, sogou_type=1):
        url_sogou_wx = ('http://wx.sogou.com/weixin?type=%d&s_from=input&ie=utf8&query=' % sogou_type)
        if (account_name is None) and (account_login is None):
            return
        if account_login:
            return url_sogou_wx + account_login
        if account_name:
            return url_sogou_wx + account_name

    def getWxSogouContext(self, query_url):
        if query_url is None:
            return
        html = unit_reqests.getHtml(query_url)
        soup = BeautifulSoup(html, 'html.parser')
        query_list = soup.find('ul', 'news-list2').find_all('li')
        # query_list = soup.find_all('div','gzh-box2')
        for itme in query_list:
            account_login = itme.find('p', 'info').find('label').get_text()
            account_name = itme.find('p', 'tit').find('a').get_text()
            account_name_url = itme.find('p', 'tit').find('a').attrs['href']

            dt0 = itme.find_all('dl')
            account_memo = dt0[0].find('dd').get_text()
            account_authname = '无'
            account_new_name = '无'
            account_new_url = '无'

            if len(dt0) == 3:
                account_authname = dt0[1].find('dd').get_text()
                account_new_name = dt0[2].find('a').get_text()
                account_new_url = dt0[2].find('a').attrs['href']
            if len(dt0) == 2:
                account_new_name = dt0[1].find('a').get_text()
                account_new_url = dt0[1].find('a').attrs['href']

            account_info = {
                'account_login': account_login,
                'account_name': account_name,
                'account_name_url': account_name_url,
                'account_authname': account_authname,
                'account_memo': account_memo,
                'account_new_name': account_new_name,
                'account_new_url': account_new_url,
            }
            print(account_info)

if __name__ == '__main__':
    wx_account().getServerWxAccount()
    wx_account().getUrlWxSogou(account_name='新华网')
    wx_account().getWxSogouContext('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=C114通信网')
