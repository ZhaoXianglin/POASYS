# encoding=utf-8
import datetime
from app.infohandle.basehandle import baseHandle
from app.infohandle.weibohandle import WeiboCapture
from app.infohandle.wechathandle import WechatCapture
from app.infohandle.rsshandle import RssHandle
from app.infohandle.newshandle import newsHandle

__author__ = 'jarvis'
class searchHandle(baseHandle):
    keyword = ''

    def __init__(self, keyword):
        self.keyword = keyword

    def getWeibo(self):
        weibo = WeiboCapture(self.keyword)
        items = weibo.getweiboinfos()
        sys_log = {
            'date': datetime.datetime.now(),
            'keyword': self.keyword,
            'type': 'weibo',
            'source': 'baidu',
            'count': items,
        }
        self.db.sys_log.insert(sys_log)

    def getWechat(self):
        wechat = WechatCapture(self.keyword)
        wechat.get_keyword_all()

    def getNews(self):
        news = newsHandle(self.keyword)
        items = news.getnewsinfos()
        sys_log = {
            'date': datetime.datetime.now(),
            'keyword': self.keyword,
            'type': 'news',
            'source': 'baidu',
            'count': items,
        }
        self.db.sys_log.insert(sys_log)

    def getAll(self):
        self.getNews()
        self.getWechat()
        self.getWeibo()

    def captureRss(self):
        rss = RssHandle()
        rss.getinfos()

    def captureWechat(self):
        wechat = WechatCapture(self.keyword)
        wechat.start()

    def captureAll(self):
        self.captureRss()
        self.captureWechat()


if __name__ == '__main__':
    test = searchHandle('长江沉船')
    test.getWechat()


