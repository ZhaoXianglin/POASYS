# encoding=utf-8

import urllib2
from bs4 import BeautifulSoup
from time import sleep
from app.infohandle.basehandle import baseHandle
from infohandle import InfoHandle
import pymongo
import jieba.analyse
from multiprocessing import Process

class WeiboCapture(baseHandle):
    # 抓取链接
    url = "http://www.baidu.com/s?wd="
    pamaurl = "&cl=2&tn=baiduwb&ie=utf-8&rtt=2&pn="
    # 伪造文件头
    send_headers = {
        'Host': 'baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    send_sina_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    conn = pymongo.Connection('127.0.0.1', 27017)
    db = conn['POASYS']
    keyword = ''

    # 初始化
    def __init__(self, keyword):
        self.keyword = keyword


    # 获取指定页面内容
    def gethtml(self, page):
        page = page-1
        page = str(page*10)
        url = self.url+self.keyword+self.pamaurl+page
        print(url)
        req = urllib2.Request(url, headers=self.send_headers)
        res = urllib2.urlopen(req)
        if res.getcode() == 200:
            html_doc = res.read()
            return html_doc
        else:
            return 0

# 获得页面数量 0表示页面存在但没有下一页，-1表示没收到参数
    def getpagenum(self):
        html_doc = self.gethtml(1)
        if html_doc != 0:
            soup = BeautifulSoup(html_doc)
            pages = soup.find('p', id='page')
            if pages:
                nextpage = pages.find('a', class_="n", text="下一页>")
                while nextpage:
                    propage = int(nextpage.previous_sibling.find('span', class_='pc').string)
                    tmp_html = self.gethtml(propage)
                    tmp_soup = BeautifulSoup(tmp_html)
                    pages = tmp_soup.find('p', id='page')
                    nextpage = pages.find('a', class_="n", text="下一页>")
                return propage
            else:
                return 0
        else:
            return -1


# 获取单页面信息
    def getpageinfo(self, page):
        html_doc = self.gethtml(page)
        if html_doc != 0:
            soup = BeautifulSoup(html_doc)
            items = soup.find_all('div', class_='weibo_detail')
            for item in items:
                countnum = item.find('div', class_='weibo_pz')
                date = self.timeformat(countnum.next_sibling.a.string)
                trans = int(countnum.contents[0].string[3:-1])
                ping = int(countnum.contents[2].string[3:-1])
                content = item.p.get_text()[:-6]
                author = item.a.string
                link = item.find('a', class_='weibo_all').get('href')
                infohandle = InfoHandle(content)
                infohandle.sentensemark()
                segment = infohandle.segment
                segmentpos = infohandle.segmentpos
                operation = infohandle.operation
                emotion = infohandle.emotion
                weibokeyword = list(jieba.analyse.extract_tags(content, 5))
                weiboinfo = {
                    'content': content,
                    'trans': trans,
                    'ping': ping,
                    'author': author,
                    'link': link,
                    'segment': segment,
                    'segmentpos': segmentpos,
                    'keyword': weibokeyword,
                    'operation': operation,
                    'emotion': emotion,
                    'search': self.keyword,
                    'date': date

                }
                print(date)
                self.db.weibo_search_results.insert(weiboinfo)
            return len(list(items))
        else:
            return -1


#获取关键词的全部数据
    def getweiboinfos(self):
        pages = self.getpagenum()
        print(pages)
        if pages > 0:
            for page in range(1, pages):
                listitem = self.getpageinfo(page)
            return listitem+pages*10
        else:
            print "数据不存在"
            return 0


#获取热点词
    def getHotWord(self):
        hoturl = "http://s.weibo.com/top/summary?cate=realtimehot"# 微博热点话题
        hotwords = []
        req = urllib2.Request(hoturl, headers=self.send_sina_headers)
        res = urllib2.urlopen(req)
        if res.getcode() == 200:
            html_doc = res.read()
        else:
            html_doc = 0
        if html_doc != 0:
            print(html_doc)
            soup = BeautifulSoup(html_doc)

            items = soup.find_all('p', class_='star_name')
            print(items)
        else:
            print("error")



if __name__ == '__main__':
    webo = WeiboCapture('长江沉船')
    webo.getweiboinfos()
