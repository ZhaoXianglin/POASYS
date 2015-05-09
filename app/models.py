__author__ = 'jarvis'
#coding:utf-8

from datetime import datetime
from .import db
class RssType(db.Document):
    id = db.StringField()

class RssFeeds(db.Document):
    rfrom = db.StringField(required=True)
    rname = db.StringField(required=True)
    rfeed = db.StringField(required=True)
    rtype = db.StringField(required=True)
    rdate = db.DateTimeField(default=datetime.now())

class RssResults(db.Document):
    rtitle = db.StringField()
    rtitle_keyword = db.ListField()
    rtitle_segment = db.ListField()
    rtitle_segment_pos = db.ListField()
    rlink = db.StringField()
    rsummary = db.StringField()
    rsummary_keyword = db.ListField()
    rsummary_segment = db.ListField()
    rpublished = db.DateTimeField()
    rfrom = db.StringField()
    rtype = db.StringField()
    roperation = db.IntField(default=0)
    remotion = db.ListField()
    rlocation = db.StringField()

