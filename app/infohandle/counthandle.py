# coding:utf-8
import datetime

__author__ = 'jarvis'
from app.infohandle.basehandle import baseHandle
from collections import Counter
class countHandle(baseHandle):
    # 词频统计
    def listcount(self, collection_name, field_name, date_field_name, date_value):
        collection = self.db[collection_name]
        items = collection.find({date_field_name: {"$gt": date_value}})
        word_list = []
        for item in items:
            if len(item[field_name]) > 0:
                word_list += item[field_name]
        dict_count = dict(Counter(word_list))
        dict_list = sorted(dict_count.iteritems(), key=lambda d: d[1], reverse=True)
        return dict_list


if __name__ == '__main__':
    test = countHandle()
    selecttime = datetime.datetime.now()-datetime.timedelta(days=3)
    print(selecttime)
    test.listcount('rss_results', 'remotion', 'rpublished', selecttime)
