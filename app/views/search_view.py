# coding:utf-8
from .import search
import datetime
from mongoengine import Q
import pymongo
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
        keyword = keyword.strip()
        newsresult = NewsResults.objects(search=keyword)
        wechatresult = WechatSearchResults.objects(search=keyword)
        weiboresult = WeiboSearchResults.objects(search=keyword)
        return render_template('search_detail.html', keyword=keyword)

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

    return jsonify(
        keywordresult=wechatresult
    )
