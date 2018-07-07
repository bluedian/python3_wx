# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
import redis
import re


class caji_test_521:
    def __init__(self):
        self.server_rds = redis.Redis('localhost', port=6379, db=0, decode_responses=True)
        self.work_url = 'http://s2.lulujjs.club/'

        self.guolu = ['hotsearch', 'login', 'register', 'action', 'mobile']
        self.three_link = 'torrent'

    def guoluUrl(self, query_url):
        if query_url is None:
            return
        for item in self.guolu:
            if query_url.find(item) > 0:
                return
        return True

    def setRedis(self, query_urls, temp_step='net_1_yes'):
        rds = self.server_rds
        if query_urls is None:
            return
        for query_url in query_urls:
            if query_url not in rds.lrange('net_yes', 0, -1):
                print(query_url)
                rds.rpush(temp_step, query_url)
                rds.rpush('net_yes', query_url)

    def getSoup(self, query_url):

        profile1=webdriver.FirefoxProfile()
        profile1.set_preference('permissions.default.stylesheet', 2)
        profile1.set_preference('permissions.default.image', 2)
        firefox = webdriver.Firefox(profile1)
        firefox.get(query_url)

        html = firefox.page_source
        firefox.close()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def word_one(self, query_url):
        url_link_all = []

        html_soup = self.getSoup(query_url)

        link_all = html_soup.find_all('a')

        for item in link_all:
            if 'href' in item.attrs:
                url_all = urljoin(self.work_url, item.attrs['href'])
                if url_all is self.work_url:
                    continue

                if url_all not in url_link_all:
                    if (url_all.find(self.work_url) == 0) and self.guoluUrl(url_all):
                        url_link_all.append(url_all)

        self.setRedis(url_link_all)

    def word_two(self, query_url):
        url_link_all = []

        html_soup = self.getSoup(query_url)

        link_all = html_soup.find_all('a')

        for item in link_all:
            if 'href' in item.attrs:
                url_all = urljoin(self.work_url, item.attrs['href'])
                if url_all is self.work_url:
                    continue

                if url_all not in url_link_all:
                    if (url_all.find(self.work_url) == 0) and self.guoluUrl(url_all):
                        url_link_all.append(url_all)

        self.setRedis(url_link_all)

    def word_three(self, query_url):
        url_link_all = []
        print(query_url)
        html_soup = self.getSoup(query_url)

        div_html = html_soup.find('div', 'pcb')

        print(div_html)

        link_html = div_html.find_all('a')

        for item in link_html:
            if 'href' in item.attrs:
                print(item.attrs['href'])

        # for item in link_all:
        #     if 'href' in item.attrs:
        #         url_all=urljoin(self.work_url,item.attrs['href'])
        #         if url_all is self.work_url:
        #             continue
        #
        #         if url_all not in url_link_all:
        #             if (url_all.find(self.work_url)==0)and self.guoluUrl(url_all):
        #                 url_link_all.append(url_all)
        #
        # self.setRedis(url_link_all)

    def lenRedis(self):
        rds = redis.Redis('localhost', port=6379, db=0, decode_responses=True)

        print('net_yes: ', rds.llen('net_yes'))
        print('net_1_yes: ', rds.llen('net_1_yes'))
        print('net_2_yes: ', rds.llen('net_2_yes'))
        print('net_3_yes: ', rds.llen('net_3_yes'))


if __name__ == '__main__':
    # caji_test_521().word_one(caji_test_521.work_url)

    caji_test_521().word_three('http://s2.lulujjs.club/thread-1225708-1-1.html')

    # caji_test_521().lenRedis()
