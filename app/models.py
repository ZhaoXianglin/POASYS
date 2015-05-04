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