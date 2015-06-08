# encoding=utf-8
import json
from string import lstrip, strip
import urllib2
from bs4 import BeautifulSoup
from app.infohandle.basehandle import baseHandle
from app.infohandle.infohandle import InfoHandle
import pymongo
import jieba.analyse
__author__ = 'jarvis'

class newsHandle(baseHandle):
    baseurl = "http://www.baidu.com/s?wd="
    extraurl = "&tn=baidurt&ie=utf-8&rtt=1&bsst=1&pn="
    send_headers = {
        'Host': 'baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    keyword = ''

    # 初始化
    def __init__(self, keyword):
        self.keyword = keyword

     # 获取指定页面内容
    def gethtml(self, page):
        page = page-1
        page = str(page*10)
        url = self.baseurl+self.keyword+self.extraurl+page
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
            items = soup.find_all('td', class_='f')
            for item in items:
                newcontent = ''
                newtitle = ''
                title = item.find('a', target="_blank").strings
                for i in title:
                    newtitle += i
                timeblock = item.find('div', class_='realtime')
                contents = list(timeblock.next_siblings)
                for num in range(0, len(contents)-1):
                    newcontent += str(contents[num].string)
                timestr = timeblock.string.split(u'-')
                if(len(timestr) > 1):
                    time = self.timeformat(lstrip(timestr[1]))
                    source = strip(timestr[0])
                else:
                    time = self.timeformat(strip(timestr[0]))
                    source = ''
                infohandle = InfoHandle(newtitle)
                infohandle.sentensemark()
                newsinfo = {
                    'title': newtitle,
                    'title_segment': infohandle.segment,
                    'title_segmentpos': infohandle.segmentpos,
                    'title_keyword': list(jieba.analyse.extract_tags(newtitle, 5)),
                    'content': newcontent,
                    'date': time,
                    'source': source,
                    'search': self.keyword,
                    'emotion': infohandle.emotion,
                    'opiniomn': infohandle.operation,
                }
                self.db.news_results.insert(newsinfo)
            return len(list(items))
        else:
            return -1

        #获取关键词的全部数据
    def getnewsinfos(self):
        pages = self.getpagenum()
        print(pages)
        if pages > 0:
            for page in range(1, pages):
                listitems = self.getpageinfo(page)
            return listitems+pages*10
        else:
            print "数据不存在"
            return 0

    # ----获取新闻热点词------
    def get_hot_words(self):
        json_url = 'http://opendata.baidu.com/api.php?resource_id=10928&query=FreshQueryList&format=json'
        req = urllib2.Request(json_url)
        res = urllib2.urlopen(req)
        if res.getcode() == 200:
            html_doc = res.read()
        jsonstr = json.loads(html_doc.decode('GBK'))
        hotwords = jsonstr['data'][0]['bdlist']
        return hotwords

if __name__ == '__main__':
    test = newsHandle('长江沉船')
    test.getnewsinfos()
