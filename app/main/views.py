__author__ = 'jarvis'
# coding:utf-8
from flask.views import MethodView
from datetime import datetime
from flask import render_template, redirect, url_for
from app.models import RssFeeds, RssResults
from . import main
from .forms import RssForm
import feedparser
import jieba
from multiprocessing import Process
from time import sleep
from ..infohandle.infohandle import InfoHandle
import jieba.analyse


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
                    titlehandle = InfoHandle(i.title)
                    titlehandle.sentensemark()
                    if hasattr(i, 'published'):
                        publishedtime = i.published
                    else:
                        publishedtime = datetime.now()
                    rssresult = RssResults(
                        rtitle=i.title,
                        rtitle_keyword=list(jieba.analyse.extract_tags(i.title, 5)),
                        rtitle_segment=titlehandle.segment,
                        rtitle_segment_pos=titlehandle.segmentpos,
                        rlink=i.link,
                        rsummary=i.summary,
                        rsummary_keyword=list(jieba.analyse.extract_tags(i.summary, 10)),
                        rsummary_segment=list(jieba.cut(i.summary, cut_all=False)),
                        rpublished=publishedtime,
                        rfrom=feed.rfrom,
                        rtype=feed.rtype,
                        roperation=titlehandle.operation,
                        remotion=titlehandle.emotion,
                    )
                    rssresult.save()
            feedcheck[num] = feedinfo.entries[0].title
        sleep(3600)
    return 'catch start'

p = Process(target=getrssinfo)

@main.route('/')
def index():
    timenow = datetime.now()
    rssinfocount = RssResults.objects().count()
    return render_template('index.html', timenow=timenow, rssinfocount=rssinfocount)


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



@main.route('/rss_get_start/')
def rssgetstart():
    p.start()
    return "开始抓取，请移步其他工作"

@main.route('/rss_get_stop/')
def rssgetstop():
    p.terminate()
    return "强制停止抓取"


@main.route('/rss_edit/<id>', methods=['GET'])
def rss_edit(id):
    form = RssForm()
    rssfeed = RssFeeds.objects(id=id)
    rssfeeds = RssFeeds.objects.all()
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds)

@main.route('/rssinfolist/', methods=['GET', 'POST'])
def rssinfolist():
    pass

class ListView(MethodView):
    def get(self):
        return render_template('index.html')

main.add_url_rule('/test', view_func=ListView.as_view('hello'))