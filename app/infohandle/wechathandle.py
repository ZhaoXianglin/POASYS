# encoding=utf-8
__author__ = 'jarvis'
import json
import urllib2
from bs4 import BeautifulSoup
from time import sleep, localtime, strftime, time
from infohandle import InfoHandle
import pymongo
import jieba.analyse
from multiprocessing import Process
import datetime

class WechatCapture(object):
    # 抓取链接
    url = "http://chuansong.me"
    search_url = "http://weixin.sogou.com/weixin?query="
    search_extraurl = "&type=2&ie=utf8&page="
    keyword = ''
    # 伪造文件头
    send_headers = {
        'Host': 'chuansong.me',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    search_send_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    conn = pymongo.Connection('202.113.78.6', 27017)
    db = conn['POASYS']

    # 初始化
    def __init__(self, keyword):
        self.keyword = keyword

    def gethtml(self, url):
        # 构造请求
        req = urllib2.Request(url, headers=self.send_headers)
        res = urllib2.urlopen(req)
        html_doc = res.read()
        return html_doc

    def getformatitem(self, url):
        html_doc = self.gethtml(url)
        soup = BeautifulSoup(html_doc)
        item = soup.find_all('a', class_="question_link")
        print('共'+str(len(item)))
        num = 0
        for i in item:
            num += 1
            print('第'+str(num)+'条')
            detailurl = self.url+i.get('href')
            detailhtml = self.gethtml(detailurl)
            detail = BeautifulSoup(detailhtml)
            title = detail.h2.string
            infohandle = InfoHandle(title)
            infohandle.sentensemark()
            title_segment = infohandle.segment
            title_segmentpos = infohandle.segmentpos
            title_keyword = list(jieba.analyse.extract_tags(title, 5))
            operation = infohandle.operation
            emotion = infohandle.emotion
            date = detail.find('em', class_='rich_media_meta rich_media_meta_text').contents[0]
            author = detail.find('a', class_='rich_media_meta rich_media_meta_link rich_media_meta_nickname').contents[0]
            record = {
                'title': title,
                'title_segment': title_segment,
                'title_segmentpos': title_segmentpos,
                'title_keyword': title_keyword,
                'operation': operation,
                'emotion': emotion,
                'date': date,
                'author': author,
                'link': detailurl
            }
            sleep(5)
            self.db.wechat_results.insert(record)

    def getstart(self):
        for page in range(0, 525, 25):
            url = self.url+'/?start='+str(page)
            print('开始抓取：'+url)
            self.getformatitem(url)

    def start(self):
        process = Process(target=self.getstart)
        process.start()
        process.join()

# -----------------------搜索部分-------------------

    def get_keyword_html(self, page):
        page = str(page)
        url = self.search_url+self.keyword+self.search_extraurl+page
        print(url)
        req = urllib2.Request(url, headers=self.search_send_headers)
        res = urllib2.urlopen(req)
        if res.getcode() == 200:
            html_doc = res.read()
            return html_doc
        else:
            return 0

    def get_keyword_pagenum(self):
        html_doc = self.get_keyword_html(1)
        if html_doc != 0:
            soup = BeautifulSoup(html_doc)
            pageblock = soup.find('div', id="pagebar_container").contents
            searchnum = soup.find('resnum', id="scd_num").string
            return {
                'pagenum': len(pageblock)-3,
                'searchnum': int(searchnum.replace(',', ''))
            }
        else:
            return 0

    #获取单页信息
    def get_keyword_page(self, page):
        html_doc = self.get_keyword_html(page)
        if html_doc != 0:
            soup = BeautifulSoup(html_doc)
            items = soup.find_all('div', class_='txt-box')
            for item in items:
                link = item.h4.a.get('href')
                title = item.h4.a.get_text()
                infohandle = InfoHandle(title)
                infohandle.sentensemark()
                summary = item.p.get_text()
                author = item.find('a', id="weixin_account").string[26:-7]
                time = localtime(float(item.find('div', class_='s-p').get('t')))
                #time = strftime('%Y-%m-%d %H:%M:%S', time)
                wechat_info = {
                    'title': title,
                    'link': link,
                    'segment': infohandle.segment,
                    'segmentpos': infohandle.segmentpos,
                    'keyword': list(jieba.analyse.extract_tags(title, 5)),
                    'opinion': infohandle.operation,
                    'emotion': infohandle.emotion,
                    'search': self.keyword,
                    'date': time,
                    'author': author,
                    'summary': summary,
                }
                self.db.wechat_search_results.insert(wechat_info)
            return len(items)
        else:
            return 0

    # 获取全部信息
    def get_keyword_all(self):
        page = self.get_keyword_pagenum()
        pagenum = page['pagenum']
        searchnum = page['searchnum']
        for i in range(1, pagenum+1):
            self.get_keyword_page(i)
        sys_log = {
            'date': datetime.datetime.now(),
            'keyword': self.keyword,
            'type': 'wechat',
            'source': 'sogou',
            'count': searchnum,
        }
        self.db.sys_log.insert(sys_log)

    # 获取今日热点
    def get_today_hotpoint(self):
        jsonurl = 'http://weixin.sogou.com/pcindex/pc/web/web.js?t='
        timestamp = str(int(time()))
        nowurl = jsonurl+timestamp
        print(nowurl)
        req = urllib2.Request(nowurl, headers=self.search_send_headers)
        res = urllib2.urlopen(req)
        if res.getcode() == 200:
            html_doc = res.read()
        jsonstr = json.loads(html_doc)
        hotwords = []
        for word in jsonstr['topwords']:
            hotwords.append(word['word'])
        return hotwords

if __name__ == '__main__':
    wechat = WechatCapture('长江沉船')
    wechat.start()


