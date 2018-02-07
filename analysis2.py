#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
import csv
import re
import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, siteurl):
        self.siteurl = siteurl
        # self.useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
        # self.useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.112 Safari/537.36 Vivaldi/1.91.867.48'
        # self.useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57'
        self.headers = {'User_agent': self.useragent}
        now = datetime.datetime.now()
        self.now = now.strftime('%y-%m-%d_%H:%M:%S')
        dirname = './csvdir/'
        filename = f'qiubai_{self.now}.csv'
        self.csvpath = f'{dirname}{filename}'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.csvpath, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('author', 'age', 'content', 'vote', 'comment', 'up', 'down'))


    def getpage(self, start=1, end=None):
        if end is None:
            end = start
        start, end = int(start), int(end)
        if start > end:
            start, end = end, start
        for page in range(start, end+1):
            if 1 < page < 35:
                pageurl = self.siteurl + f'/page/{page}/'
            elif page >= 35:
                pageurl = self.siteurl + '/page/35/'
            elif page <= 1:
                pageurl = self.siteurl
            self.analysis(pageurl)

    def analysis(self, url):
        pagereq = requests.get(url, headers=self.headers)
        if pagereq.status_code == 200:
            pagesoup = BeautifulSoup(pagereq.text, 'lxml')
            for item in pagesoup.find_all('div', {'class': re.compile('article.*mb15')}):
                self.parse(item)

    def parse(self, soup):
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
        self.savecsv(row)

    def savecsv(self, row):
        with open(self.csvpath, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)


def main():
    option = sys.argv
    spider = Spider(option[1])
    spider.getpage(*option[2:4])


if __name__ == '__main__':
    main()
