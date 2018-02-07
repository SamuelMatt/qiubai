#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import csv
import re
import requests
from bs4 import BeautifulSoup

useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
# useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
# useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.112 Safari/537.36 Vivaldi/1.91.867.48'
# useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57'
headers = {'User_agent': useragent}
now = datetime.datetime.now()
now = now.strftime('%y-%m-%d_%H:%M:%S')
dirname = './csvdir/'
filename = f'qiubai_{now}.csv'


def getpage(siteurl, start=1, end=None):
    if end is None:
        end = start
    start, end = int(start), int(end)
    if start > end:
        start, end = end, start
    for num in range(start, end+1):
        if 1 < num < 35:
            pageurl = siteurl + f'/page/{num}/'
        elif num >= 35:
            pageurl = siteurl + '/page/35/'
        elif num <= 1:
            pageurl = siteurl
        analysis(pageurl)


def analysis(url):
    pagereq = requests.get(url, headers=headers)
    if pagereq.status_code == 200:
        pagesoup = BeautifulSoup(pagereq.text, 'lxml')
        for item in pagesoup.find_all('div', {'class': re.compile('article.*mb15')}):
            parse(item)


def parse(soup):
    author = soup.h2.get_text()
    author = author.strip()
    content = soup.find('div', {'class', re.compile('content')}).span.get_text()
    content = content.strip()
    try:
        age = soup.find('div', {'class': re.compile('article.*Icon')}).get_text()
    except AttributeError as e:
        age = '0'
    vote = soup.find('span', {'class': re.compile('stats-vote')}).i.get_text()
    comment = soup.find('a', {'class': re.compile('qiushi_comments')}).i.get_text()
    up = soup.find('li', {'class': re.compile('up')}).find('span', {'class': re.compile('number hidden')}).get_text()
    down = soup.find('li', {'class': re.compile('down')}).find('span', {'class': re.compile('number hidden')}).get_text()
    row = (author, age, content, vote, comment, up, down)
    savecsv(row)


def  savecsv(row):
    with open(f'{dirname}{filename}', 'a+') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def main():
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(f'{dirname}{filename}', 'a+') as file:
        writer = csv.writer(file)
        writer.writerow(('author', 'age', 'content', 'vote', 'comment', 'up', 'down'))
    getpage(*sys.argv[1:4])


if __name__ == '__main__':
    main()
