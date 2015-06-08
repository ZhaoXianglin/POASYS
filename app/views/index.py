__author__ = 'jarvis'
# coding:utf-8
from .import home
from flask import render_template, jsonify
import datetime
from ..models import RssResults, WechatResults, WeiboResults, EmotionDict
from app.infohandle.rsshandle import RssHandle
from mongoengine import Q


@home.route('/')
def index():
    timenow = datetime.datetime.now()
    todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
    rssinfocount = RssResults.objects().count()
    weichatcount = WechatResults.objects().count()
    weibocount = WeiboResults.objects().count()
    dictcount = EmotionDict.objects.count()
    todaycount = RssResults.objects(rpublished__gte=todayzero).count()
    countinfo = {
        'rss': rssinfocount, # rss源数据统计
        'dict': dictcount,  # 字典数据统计
        'weibo': weibocount, # 微博数据统计
        'wechat': weichatcount, # 微信数据统计
        'today': todaycount,#RSS今天数据
    }
    news = RssResults.objects().order_by('-rpublished')[:7]
    wechats = WechatResults.objects().order_by('-date')[:7]

    return render_template('index.html', timenow=timenow, info=countinfo, news=news, wechats=wechats)

@home.route('/ajax/indexguage/', methods=['get', 'post'])
def returnindexguage():
    todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
    positivenum = RssResults.objects(Q(rpublished__gte=todayzero) & Q(roperation__gt=0)).count()
    negativenum = RssResults.objects(Q(rpublished__gte=todayzero) & Q(roperation__lt=0)).count()
    todaymention = RssResults.objects(rpublished__gte=todayzero).count()
    return jsonify(
        positivenum=positivenum,
        negativenum=negativenum,
        todaymention=todaymention
    )
@home.route('/ajax/indexline/', methods=['get', 'post'])
def returnindexline():
    todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
    today = datetime.datetime.today()
    date = [todayzero]
    week = [today.strftime('%a')]
    positivenum = [RssResults.objects(Q(rpublished__gte=todayzero) & Q(roperation__gt=0)).count()]
    negativenum = [RssResults.objects(Q(rpublished__gte=todayzero) & Q(roperation__lt=0)).count()]
    todaymention = [RssResults.objects(rpublished__gte=todayzero).count()-positivenum[0]-negativenum[0]]
    for day in range(1, 7):
        week.append((today-datetime.timedelta(days=day)).strftime('%a'))
        date.append(todayzero-datetime.timedelta(days=day))
        positivenum.append(RssResults.objects(Q(rpublished__gte=date[day]) & Q(rpublished__lt=date[day-1]) & Q(roperation__gt=0)).count())
        negativenum.append(RssResults.objects(Q(rpublished__gte=date[day]) & Q(rpublished__lt=date[day-1]) & Q(roperation__lt=0)).count())
        todaymention.append(RssResults.objects(Q(rpublished__gte=date[day]) & Q(rpublished__lt=date[day-1])).count()-positivenum[day]-negativenum[day])
    return jsonify(
        positivenum=positivenum,
        negativenum=negativenum,
        todaymention=todaymention,
        week=week,
        date=date,
    )


@home.route('/test/')
def test():
    item = RssHandle()
    return render_template('index.html', timenow=item.getinfos())
    #return 'hello'
