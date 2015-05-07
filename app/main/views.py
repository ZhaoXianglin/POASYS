__author__ = 'jarvis'
# coding:utf-8
from datetime import datetime
from flask import render_template, redirect, url_for, request

from app.models import RssFeeds, RssResults
from . import main
from .forms import RssForm
import feedparser
import jieba
from multiprocessing import Process
from time import sleep
import jieba.analyse
import jieba.posseg as pseg
def getrssinfo():
    rssfeeds = RssFeeds.objects.all()
    feedcheck = []
    for i in range(len(rssfeeds)):
        feedcheck.append('check')

    while True:
        for num, feed in enumerate(rssfeeds):
            feedinfo = feedparser.parse(feed.rfeed)
            if feedcheck[num] != feedinfo.entries[0].title:
                for i in feedinfo.entries:
                    title_segment_list = []
                    title_segment = pseg.cut(i.title)
                    for segment in title_segment:
                        title_segment_list.append((segment.word, segment.flag))
                    rssresult = RssResults(
                        rtitle=i.title,
                        rtitle_keyword=list(jieba.analyse.extract_tags(i.title, 5)),
                        rtitle_segment=list(jieba.cut(i.title)),
                        rtitle_segment_pos=title_segment_list,
                        rlink=i.link,
                        rsummary=i.summary,
                        rsummary_keyword=list(jieba.analyse.extract_tags(i.summary, 10)),
                        rsummary_segment=list(jieba.cut(i.summary, cut_all=False)),
                        rpublished=i.published,
                        rfrom=feed.rfrom,
                        rname=feed.rname
                    )
                    rssresult.save()
            feedcheck[num] = feedinfo.entries[0].title
        sleep(3600)
    return 'catch start'

p = Process(target=getrssinfo)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/rss_setting/<page>', methods=['GET', 'POST'])
def rss_setting(page=1):
    page = int(page)
    form = RssForm()
    pagination = RssFeeds.objects.paginate(page=page, per_page=10, error_out=False)
    rssfeeds = pagination.items
    if form.validate_on_submit():
        rssfeed = RssFeeds(
            rfrom=form.rfrom.data,
            rname=form.rname.data,
            rfeed=form.rfeed.data,
            rtype=form.rtype.data,
            rdate=datetime.now()
        )
        rssfeed.save()
        return redirect(url_for('.rss_setting', page=1))
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds, pagination=pagination)

@main.route('/rss_page/<page>', methods=['GET'])
def rss_page(page):
    page = int(page)
    pagination = RssFeeds.objects.paginate(page=page, per_page=10, error_out=True)
    rssfeeds = pagination.items
    return render_template('rss_page.html', rssfeeds=rssfeeds, pagination=pagination)

@main.route('/rss_get_start/')
def rssgetstart():
    p.start()
    return "hello"

@main.route('/rss_get_stop/')
def rssgetstop():
    p.terminate()
    return "stop"


@main.route('/rss_edit/<id>', methods=['GET'])
def rss_edit(id):
    form = RssForm()
    rssfeed = RssFeeds.objects(id=id)
    rssfeeds = RssFeeds.objects.all()
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds)

@main.route('/rssinfolist/', methods=['GET', 'POST'])
def rssinfolist():
    pass

