__author__ = 'jarvis'
#coding:utf-8

from datetime import datetime
from .import db
class RssType(db.Document):
    id = db.StringField()
# RSS源
class RssFeeds(db.Document):
    rfrom = db.StringField(required=True)
    rname = db.StringField(required=True)
    rfeed = db.StringField(required=True)
    rtype = db.StringField(required=True)
    rdate = db.DateTimeField(default=datetime.now())

# rss抓取结果
class RssResults(db.Document):
    rtitle = db.StringField()
    rtitle_keyword = db.ListField(db.StringField())
    rtitle_segment = db.ListField(db.StringField())
    rtitle_segment_pos = db.ListField(db.DictField())
    rlink = db.StringField()
    rsummary = db.StringField()
    rsummary_keyword = db.ListField(db.StringField())
    rsummary_segment = db.ListField(db.StringField())
    rpublished = db.DateTimeField()
    rfrom = db.StringField()
    rtype = db.StringField()
    roperation = db.IntField(default=0)
    remotion = db.ListField(db.StringField())
    rlocation = db.StringField()

# 微信数据
class WechatResults(db.Document):
    title = db.StringField()
    title_keyword = db.ListField()
    title_segment = db.ListField()
    title_segmentpos = db.ListField()
    link = db.StringField()
    author = db.StringField()
    date = db.DateTimeField()
    operation = db.IntField(default=0)
    emotion = db.ListField()

# 微博数据
class WeiboResults(db.Document):
    trans = db.IntField()
    ping = db.IntField()
    keyword = db.ListField()
    content = db.StringField()
    segment = db.ListField()
    segmentpos = db.ListField()
    link = db.StringField()
    author = db.StringField()
    date = db.DateTimeField()
    operation = db.IntField(default=0)
    emotion = db.ListField()


class EmotionDict(db.Document):
    dpolar = db.IntField() #极性
    dword = db.StringField()
    dstengthother = db.IntField()
    dpolarother = db.IntField()
    demotionother = db.StringField()
    dstength = db.IntField()
    dwordmeans = db.IntField()
    demotiontype = db.StringField()
    dmeannum = db.IntField()
    dwordtype = db.StringField()

    meta = {'collection': 'emotiondict'}

class SearchResults(db.Document):
    word = db.StringField()
    jointime = db.DateTimeField()
    updatetime = db.DateTimeField()

class NewsResults(db.Document):
    emotion = db.ListField()
    title_segment = db.ListField()
    title_keyword = db.ListField()
    opiniomn = db.IntField(default=0)
    date = db.DateTimeField()
    title_segmentpos = db.ListField()
    search = db.StringField()
    title = db.StringField()
    content = db.StringField()
    source = db.StringField()
    meta = {'collection': 'news_results'}

class WechatSearchResults(db.Document):
    emotion = db.ListField()
    link = db.StringField()
    date = db.DateTimeField()
    segment = db.ListField()
    segmentpos = db.ListField()
    search = db.StringField()
    keyword = db.ListField()
    title = db.StringField()
    author = db.StringField()
    summary = db.StringField()
    opinion = db.IntField(default=0)

    meta = {'collection': 'wechat_search_results'}

class WeiboSearchResults(db.Document):
    emotion = db.ListField()
    link = db.StringField()
    date = db.DateTimeField()
    operation = db.IntField(default=0)
    segment = db.ListField()
    segmentpos = db.ListField()
    search = db.StringField()
    keyword = db.ListField()
    author = db.StringField()
    ping = db.IntField(default=0)
    content = db.StringField()
    trans = db.IntField(default=0)

    meta = {'collection': 'weibo_search_results'}



