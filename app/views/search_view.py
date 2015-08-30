# coding:utf-8
from .import search
import datetime
from multiprocessing import Process
from mongoengine import Q
from app.infohandle.counthandle import countHandle
from app.infohandle.searchhandle import searchHandle
from app.models import SearchResults, NewsResults, WechatSearchResults, WeiboSearchResults
from flask import render_template, redirect, url_for, request, jsonify

__author__ = 'jarvis'

@search.route('/<page>/', methods=['GET'])
def index(page=1):
    page = int(page)
    pagination = SearchResults.objects.paginate(page=page, per_page=10, error_out=False)
    searchword = pagination.items
    return render_template('search_index.html', searchword=searchword, pagination=pagination)

@search.route('/additem/', methods=['POST'])
def additem():
    if request.method == 'POST' and len(request.form['keyword']) > 0:
        keyword=request.form['keyword'].strip(),
        searchword = SearchResults(
            word=request.form['keyword'].strip(),
            jointime=datetime.datetime.now(),
            updatetime=datetime.datetime.now(),
        )
        searchword.save()
        return redirect(url_for('search.index', page=1))
    else:
        return redirect(url_for('home.index'))

@search.route('/detail/<keyword>', methods=['GET', 'POST'])
def detail(keyword):
    if len(keyword) > 0:
        newsresultup = NewsResults.objects(search=keyword).order_by('-opiniomn')[:10]
        newsresultdown = NewsResults.objects(search=keyword).order_by('opiniomn')[:10]
        wechatresultdown = WechatSearchResults.objects(search=keyword).order_by('opinion')[:10]
        weiboresultdown = WeiboSearchResults.objects(search=keyword).order_by('operation')[:10]
        wechatresultup = WechatSearchResults.objects(search=keyword).order_by('-opinion')[:10]
        weiboresultup = WeiboSearchResults.objects(search=keyword).order_by('-operation', '-trans')[:10]
        return render_template('search_detail.html', keyword=keyword,
                               newsresultup=newsresultup, wechatresultup=wechatresultup, weiboresultup=weiboresultup,
                               newsresultdown=newsresultdown, wechatresultdown=wechatresultdown, weiboresultdown=weiboresultdown)



@search.route('/ajax/detail/linechart/<keyword>', methods=['GET', 'POST'])
def linechart(keyword):
    keyword = keyword.strip()
    if len(keyword) > 0:
        todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
        today = datetime.datetime.today()
        date = [todayzero]
        week = [today.strftime('%a')]
        positivenum = [NewsResults.objects(Q(date__gte=todayzero)&Q(search=keyword)).count()]
        negativenum = [WeiboSearchResults.objects(Q(date__gte=todayzero)&Q(search=keyword)).count()]
        todaymention = [WechatSearchResults.objects(Q(date__gte=todayzero)&Q(search=keyword)).count()]
        for day in range(1, 7):
            week.append((today-datetime.timedelta(days=day)).strftime('%a'))
            date.append(todayzero-datetime.timedelta(days=day))
            positivenum.append(NewsResults.objects(Q(date__gte=date[day]) & Q(date__lt=date[day-1])&Q(search=keyword)).count())
            negativenum.append(WeiboSearchResults.objects(Q(date__gte=date[day]) & Q(date__lt=date[day-1])&Q(search=keyword)).count())
            todaymention.append(WechatSearchResults.objects(Q(date__gte=date[day]) & Q(date__lt=date[day-1])&Q(search=keyword)).count())
        return jsonify(
            newsresult=positivenum,
            weiboresult=negativenum,
            wechatresult=todaymention,
            week=week,
            date=date,
        )

@search.route('/ajax/detail/gauge/<keyword>', methods=['GET', 'POST'])
def gaugechart(keyword):
    keyword = keyword.strip()
    if len(keyword) > 0:
        todayzero = datetime.datetime.combine(date=datetime.date.today(), time=datetime.time.min)
        positivenum = NewsResults.objects(Q(date__gte=todayzero) & Q(opiniomn__gt=0)&Q(search=keyword)).count()
        negativenum = NewsResults.objects(Q(date__gte=todayzero) & Q(opiniomn__lt=0)&Q(search=keyword)).count()
        todaymention = NewsResults.objects(Q(date__gte=todayzero)&Q(search=keyword)).count()
        return jsonify(
            positivenum=positivenum,
            negativenum=negativenum,
            todaymention=todaymention
        )


@search.route('/ajax/detail/emotion/<keyword>', methods=['GET', 'POST'])
def emotionchart(keyword):
    keyword = keyword.strip()
    if len(keyword) > 0:
        counthandle = countHandle()
        selecttime = datetime.date.today()-datetime.timedelta(days=3)
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


@search.route('/count/', methods=['GET', 'POST'])
def searchcount():
        newsresult = NewsResults.objects().count()
        wechatresult = WechatSearchResults.objects().count()
        weiboresult = WeiboSearchResults.objects().count()
        return render_template('search_count.html', newsresult=newsresult, wechatresult=wechatresult,weiboresult=weiboresult)

@search.route('/ajax/count/', methods=['GET', 'POST'])
def drawcountchart():
    todayvalue = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    keywordresult = []
    newsresult = []
    wechatresult = []
    weiboresult = []
    datevalue = [todayvalue]
    searchresult = SearchResults.objects()
    # 获取一周时间
    for time in range(1, 7):
        temptime = todayvalue-datetime.timedelta(days=time)
        datevalue.append(temptime)
    for i in searchresult:
        keywordresult.append(i['word'])
    for word in keywordresult:
        daywechat = [
            {
                'time': todayvalue,
                'value': WechatSearchResults.objects(Q(date__gt=datevalue[0]) & Q(search=word)).count()}]
        daynews = [
            {
                'time': todayvalue,
                'value': NewsResults.objects(Q(date__gt=datevalue[0]) & Q(search=word)).count()}]
        dayweibo = [{
                'time': todayvalue,
                'value': WeiboSearchResults.objects(Q(date__gt=datevalue[0]) & Q(search=word)).count()}]
        for item in range(1, len(datevalue)):
            countnews = NewsResults.objects(Q(date__gte=datevalue[item]) & Q(date__lt=datevalue[item-1]) & Q(search=word)).count()
            countwechat = WechatSearchResults.objects(Q(date__lt=datevalue[item-1]) & Q(search=word)).count()
            countweibo = WeiboSearchResults.objects(Q(date__gte=datevalue[item]) & Q(date__lt=datevalue[item-1]) & Q(search=word)).count()
            daynews.append({
                'time': datevalue[item],
                'value': countnews
            })
            daywechat.append({
                'time': datevalue[item],
                'value': countwechat
            })
            dayweibo.append({
                'time': datevalue[item],
                'value': countweibo
            })

        newsresult.append({
            "name": word,
            "weight": 123,
            "evolution": daynews
        })
        wechatresult.append({
            "name": word,
            "weight": 123,
            "evolution": daywechat
        })
        weiboresult.append({
            "name": word,
            "weight": 123,
            "evolution": dayweibo
        })

    wechatjson = {
        'name': "微信声量",
        'type': "eventRiver",
        'weight': 123,
        'data': wechatresult
    }
    weibojson = {
        'name': "微博声量",
        'type': "eventRiver",
        'weight': 123,
        'data': weiboresult
    }
    newsjson = {
        'name': "新闻声量",
        'type': "eventRiver",
        'weight': 123,
        'data': newsresult
    }

    return jsonify(
        series=[wechatjson, newsjson, weibojson]
    )
