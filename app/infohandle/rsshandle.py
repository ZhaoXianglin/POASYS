__author__ = 'jarvis'
# coding:utf-8
from app.models import RssResults, RssFeeds
import feedparser
from datetime import datetime
import jieba
import jieba.analyse
from infohandle import InfoHandle
from basehandle import baseHandle
from dateutil.parser import parse

class RssHandle(baseHandle):

    #时间格式化
    def timeformat(self,protime):
        newtime = parse(protime)
        newtime = newtime.replace(tzinfo=None)
        return newtime

    # 返回rssfeed查询集合
    def getfeeds(self):
        rssfeeds = self.db['rss_feeds'].find()
        return rssfeeds

    # 返回rssfeed数量
    def feedsnum(self):
        rssfeeds = self.db['rss_feeds']
        num = rssfeeds.find().count()
        return num

    # 获取指定地址信息
    def getinfo(self, rssfeed,checktime):
        newtime = checktime
        source = feedparser.parse(rssfeed['rfeed'])
        for item in source.entries:
            if self.timeformat(item.published) > checktime:
                if newtime < self.timeformat(item.published):
                    newtime = self.timeformat(item.published)
                titlehandle = InfoHandle(item.title)
                titlehandle.sentensemark()
                initem = dict(
                    rtitle=item.title,
                    rtitle_keyword=list(jieba.analyse.extract_tags(item.title, 5)),
                    rtitle_segment=titlehandle.segment,
                    rtitle_segment_pos=titlehandle.segmentpos,
                    rlink=item.link,
                    rsummary=item.summary,
                    rpublished=self.timeformat(item.published),
                    rfrom=rssfeed['rfrom'],
                    rtype=rssfeed['rtype'],
                    roperation=titlehandle.operation,
                    remotion=titlehandle.emotion,
                )
                self.db.rss_results.insert(initem)
            else:
                continue
            self.db.rss_feeds.update({"_id": rssfeed['_id']}, {"$set": {"rdate": newtime}})
        return newtime

    #获取全部信息
    def getinfos(self):
        feeds = self.getfeeds()
        for feed in feeds:
            self.getinfo(feed, feed['rdate'])
        return 1

if __name__ == '__main__':
    rsstest = RssHandle()
    print rsstest.getinfos()

