__author__ = 'jarvis'
# coding:utf-8
import pymongo
import datetime

class baseHandle(object):
    conn = pymongo.Connection('202.113.78.6', 27017)
    db = conn['POASYS']

    def timeformat(self, strtime):
        formatdatetime = datetime.datetime.now()
        mainstr = strtime[:-1]
        daystr = mainstr[-1]
        if daystr == u"天":
            subday = int(mainstr[0])
            day = datetime.timedelta(days=subday)
            formatdatetime = datetime.datetime.now()-day
            return formatdatetime
        else:
            minstr = mainstr[-2:]
            if minstr == u"小时":
                subhour = int(mainstr[:-2])
                hour = datetime.timedelta(hours=subhour)
                formatdatetime = datetime.datetime.now()-hour
                return formatdatetime
            if minstr ==u"分钟":
                submin = int(mainstr[:-2])
                minute = datetime.timedelta(minutes=submin)
                formatdatetime = datetime.datetime.now()-minute
                return formatdatetime
            else:
                return 0

if __name__ == '__main__':
    test = baseHandle()
    print test.timeformat(u"11")