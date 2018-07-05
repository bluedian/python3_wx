# -*- coding: utf-8 -*-
from unit import unit_reqests
from bs4 import BeautifulSoup
import json
import time
import math


class wx_account():
    def __init__(self):
        self.varsion = '1.0.1'
        self.wx_account = ''
        self.wx_account_name = ''
        self.wx_account_authname = ''
        self.wx_account_memo = ''
        self.server_address = 'http://www.123.com/index.php/wx/'
        #self.server_address = 'http://oa.9oe.com/index.php/wx/'

    def synsServer(self, data=None):
        mod = 'apiaccount/'
        if data is None:
            data = {}
            data['model'] = 'get_wx_account_key'
        url_server_all = self.server_address + mod
        html = unit_reqests.postHtmlData(url_server_all, data=data)
        return html

    def synsServerUpdateAccountKey(self, data=None):
        mod = 'apiaccount/'
        if data is None:
            data = {}
            data['model'] = 'update_wx_account_key'
        url_server_all = self.server_address + mod
        html = unit_reqests.postHtmlData(url_server_all, data=data)
        return html

    def synsServerError(self, data=None):
        mod = 'apiaccount/'
        if data is None:
            data = {}
            data['model'] = 'error_account'
        url_server_all = self.server_address + mod
        unit_reqests.postHtmlData(url_server_all, data=data)

    def getUrlWxSogou(self, account_name=None, account_login=None, sogou_type=1):
        url_sogou_wx = ('http://wx.sogou.com/weixin?type=%d&s_from=input&ie=utf8&query=' % sogou_type)
        if (account_name is None) and (account_login is None):
            return
        if account_login:
            return url_sogou_wx + account_login
        if account_name:
            return url_sogou_wx + account_name

    def findWxSogou(self, query_url):
        if query_url is None:
            return
        html = unit_reqests.getHtml(query_url)
        soup = BeautifulSoup(html, 'html.parser')
        query_list = [query_url]
        query_num = 0
        try:
            if soup.find('div', 'mun') is None:
                # print('判断有几页')
                one_soup = soup.find('ul', 'news-list2')
                if one_soup is None:
                    # print('判断有几条')
                    return query_list, query_num
                else:
                    query_num = len(one_soup.find_all('li'))
                return query_list, query_num

            query_list_str = soup.find('div', 'mun').get_text()
            page_all = int(math.ceil(int(query_list_str[3:-3]) / 10))
            query_num = int(query_list_str[3:-3])
            if page_all > 10:
                page_all = 11
            for page in range(2, page_all):
                new_query_url = query_url + '&page=' + str(page)
                query_list.append(new_query_url)

        except:
            one_soup = soup.find('ul', 'news-list2')
            if one_soup:
                two_soup = one_soup.find_all('li')
                print('在这里', len(two_soup))
            print('在这里111', one_soup)

        return query_list, query_num

    def getWxSogouContext(self, query_url, acc_name=None):
        if query_url is None:
            return
        html = unit_reqests.getHtml(query_url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            query_list = soup.find('ul', 'news-list2').find_all('li')
            print(query_list)
            for itme in query_list:
                account_login = itme.find('p', 'info').find('label').get_text()
                account_name = itme.find('p', 'tit').find('a').get_text()
                account_name_url = itme.find('p', 'tit').find('a').attrs['href']
                account_source = 2
                if acc_name and (account_name == acc_name):
                    account_source = 1

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
                    try:
                        account_new_name = dt0[1].find('a').get_text()
                        account_new_url = dt0[1].find('a').attrs['href']
                    except:
                        account_authname = dt0[1].find('dd').get_text()

                account_info = {
                    'model': 'update_wx_account',
                    'account_source': account_source,
                    'account_login': account_login,
                    'account_name': account_name,
                    'account_name_url': account_name_url,
                    'account_authname': account_authname,
                    'account_memo': account_memo,
                    'account_new_name': account_new_name,
                    'account_new_url': account_new_url,
                }
                # print(account_info)
                print(wx_account().synsServer(data=account_info))
        except:
            return

    def run(self):
        run_jobs = self.synsServer()
        print(run_jobs)
        run_josn = json.loads(run_jobs)
        print(run_josn)
        if run_josn['list'] > 0:
            for subitme in run_josn['data']:
                find_url = self.getUrlWxSogou(account_name=subitme['name'])
                find_list,find_num = self.findWxSogou(find_url)
                if find_num==0:
                    data={
                        'model':'update_wx_account_key',
                        'name':subitme['name'],
                        'number':0,
                        'id':subitme['id'],
                    }
                    print(wx_account().synsServer(data=data))
                    break
                for item_url in find_list:
                    self.getWxSogouContext(item_url, acc_name=subitme['name'])
                    print(item_url)
                    time.sleep(1)
                # exit()


if __name__ == '__main__':
    wx_account().run()
    #print(wx_account().findWxSogou('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=二更'))
    #print(wx_account().findWxSogou('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=新华网'))
    #print(wx_account().findWxSogou('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=扬子晚报'))
    #print(wx_account().findWxSogou('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=sfsfsfffsfsfsdfd'))
    #print(wx_account().synsServer())
    # wx_account().getUrlWxSogou(account_name='新华网')
    # wx_account().getWxSogouContext('http://wx.sogou.com/weixin?type=1&s_from=input&ie=utf8&query=C114通信网')
