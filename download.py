#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import threading
# from queue import Queue
import requests
from bs4 import BeautifulSoup


useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
# useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
# useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.112 Safari/537.36 Vivaldi/1.91.867.48'
# useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57'
headers = {'User_agent': useragent}


def getpage(siteurl, start=1, end=None):
    if end is None:
        end = start
    start, end = int(start), int(end)
    if start > end:
        start, end = end, start
    for num in range(start, end+1):
        if 1 < num < 35:
            pageurl = siteurl + f'/page/{num}'
        elif num >= 35:
            pageurl = siteurl + '/page/35'
        elif num <= 1:
            pageurl = siteurl
        pageworker(pageurl)


def pageworker(url):
    t = threading.Thread(target=getimg, args=(url,), name='get({url})')
    t.start()


def getimg(url):
    pagereq = requests.get(url, headers=headers)
    if pagereq.status_code == 200:
        pagesoup = BeautifulSoup(pagereq.text, 'lxml')
        contentsoup = pagesoup.find('div', {'id': 'content-left'})
        for item in contentsoup.find_all('div', {'class': 'thumb'}):
            item = item.find('img', {'src': re.compile('.*\.jpg$')})
            picurl = item['src'].replace('//', 'http://')
            saveimg(picurl)


def saveimg(url):
    if not os.path.exists('./image'):
        os.mkdir('./image')
    picname = url.split('/')[-1]
    picpath = './image/' + picname
    picreq = requests.get(url, headers=headers, stream=True)
    if picreq.status_code == 200:
        with open(picpath, 'wb') as file:
            for chunk in picreq.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)


def main():
    getpage(*sys.argv[1:4])


if __name__ == '__main__':
    main()
