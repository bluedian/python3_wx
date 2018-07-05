# -*- coding: utf-8 -*-


import requests
import os
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}


def getHtml(query_url, dubeg=False):
    if query_url is None:
        return
    req = requests.get(query_url, headers=headers)
    req.encoding = req.apparent_encoding
    html = req.text
    if dubeg:
        print('调试-----start------>')
        print(query_url)
        print(html)
        print(req.status_code)
        print('调试-----end------>')
    if req.status_code == 200:
        return html
    print('error-->URL:'+query_url)
    return req.status_code


def postHtmlData(query_url, data=None, dubeg=False):
    if query_url is None:
        return
    if data:
        req = requests.post(query_url, data=data, headers=headers)
    else:
        req = requests.post(query_url)
    req.encoding = req.apparent_encoding
    html = req.text
    if dubeg:
        print('调试-----start------>')
        print(query_url)
        print(html)
        print(req.status_code)
        print('调试-----end------>')
    if req.status_code == 200:
        return html
    return req.status_code
