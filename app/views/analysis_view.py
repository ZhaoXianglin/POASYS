# coding:utf-8
from app.infohandle.counthandle import countHandle

__author__ = 'jarvis'

from app.infohandle.newshandle import newsHandle
from app.infohandle.wechathandle import WechatCapture
from .import analysis
from flask import render_template, jsonify
import datetime
from ..models import RssResults, WechatResults, WeiboResults, EmotionDict
from app.infohandle.rsshandle import RssHandle
from mongoengine import Q

@analysis.route('/news/')
def index():
    todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
    positivenews = RssResults.objects(rpublished__gte=todayzero).order_by('-roperation')[:10]
    negativenews = RssResults.objects(rpublished__gte=todayzero).order_by('roperation')[:10]
    hotpoints = newsHandle('1').get_hot_words()[:10]
    return render_template('analysis_news.html', negativenews=negativenews, positivenews=positivenews, hotpoints=hotpoints)

@analysis.route('/ajax/news/bar/', methods=['get', 'post'])
def newsbar():
    hotpoints = newsHandle('1').get_hot_words()[:10]
    words = []
    values =[]
    for item in hotpoints:
        words.append(item['content'])
        values.append(item['num'])
    words.reverse()
    values.reverse()
    return jsonify(
        words=words,
        values=values,
    )

@analysis.route('/ajax/news/wordcloud/', methods=['get', 'post'])
def newswordcloud():
    hotpoints = newsHandle('1').get_hot_words()[:10]
    data = []
    for item in hotpoints:
        data.append({
            'name': item['content'],
            'value': item['num'],
        })
    return jsonify(
        data=data,
    )
@analysis.route('/ajax/news/keyword/', methods=['get', 'post'])
def newskeyword():
    counthandle = countHandle()
    selecttime = datetime.datetime.now()-datetime.timedelta(days=1)
    data = counthandle.listcount('rss_results', 'rtitle_keyword', 'rpublished', selecttime)
    countnum = 0
    countword = []
    countvalue = []
    for num in range(0, len(data)):
        countnum += data[num][1]
    for i in range(0, 9):
        if data[i][0].isdigit():
            data.pop(i)
    data = data[0:9]
    for item in data:
        countvalue.append(item[1])
        countword.append(item[0])
    return jsonify(
        countword=countword,
        countvalue=countvalue,
        countnum=countnum
    )

@analysis.route('/ajax/news/emotion/', methods=['get', 'post'])
def newsemotion():
    counthandle = countHandle()
    selecttime = datetime.datetime.now()-datetime.timedelta(days=1)
    data = counthandle.listcount('rss_results', 'remotion', 'rpublished', selecttime)
    data = data[0:6]
    countword = []
    countvalue = []
    maxvalue = data[0][1]
    for item in data:
        countvalue.append(item[1])
        countword.append(
            {'text': item[0], 'max': maxvalue}
        )

    return jsonify(
        countword=countword,
        countvalue=countvalue,
    )

# －－－－－－－－微信部分－－－－－－－

@analysis.route('/wechat/')
def wechatindex():
    positivenews = WechatResults.objects().order_by('-date', '-operation')[:10]
    negativenews = WechatResults.objects().order_by('-date', 'operation')[:10]
    return render_template('analysis_wechat.html', negativenews=negativenews, positivenews=positivenews)

@analysis.route('/ajax/wechat/bar/', methods=['get', 'post'])
def wechatbar():
    hotpoints = WechatCapture('1').get_today_hotpoint()[:10]
    wechatvalue = [10, 10, 7, 7, 5, 5, 5, 3, 3, 1]
    return jsonify(
        words=hotpoints,
        values=wechatvalue,
    )

@analysis.route('/ajax/wechat/wordcloud/', methods=['get', 'post'])
def wechatwordcloud():
    hotpoints = WechatCapture('1').get_today_hotpoint()[:10]
    data = []
    wechatvalue = [10, 10, 7, 7, 5, 5, 5, 3, 3, 1]
    for item in range(0, len(wechatvalue)):
        data.append({
            'name': hotpoints[item],
            'value': wechatvalue[item]*1000,
        })
    return jsonify(
        data=data,
    )
@analysis.route('/ajax/wechat/keyword/', methods=['get', 'post'])
def wechatkeyword():
    counthandle = countHandle()
    selecttime = datetime.datetime.today()-datetime.timedelta(days=1)
    selecttime = selecttime.isoformat()
    data = counthandle.listcount('wechat_results', 'title_keyword', 'date', selecttime)
    countnum = 0
    countword = []
    countvalue = []
    for num in range(0, len(data)):
        countnum += data[num][1]
    for i in range(0, 9):
        if data[i][0].isdigit():
            data.pop(i)
    data = data[0:9]
    for item in data:
        countvalue.append(item[1])
        countword.append(item[0])
    return jsonify(
        countword=countword,
        countvalue=countvalue,
        countnum=countnum
    )


@analysis.route('/ajax/wechat/emotion/', methods=['get', 'post'])
def wechatemotion():
    counthandle = countHandle()
    selecttime = datetime.date.today()-datetime.timedelta(days=1)
    selecttime = selecttime.isoformat()
    data = counthandle.listcount('wechat_results', 'emotion', 'date', selecttime)
    data = data[0:6]
    countword = []
    countvalue = []
    maxvalue = data[0][1]
    for item in data:
        countvalue.append(item[1])
        countword.append(
            {'text': item[0], 'max': maxvalue}
        )

    return jsonify(
        countword=countword,
        countvalue=countvalue,
    )
