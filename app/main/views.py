__author__ = 'jarvis'
# coding:utf-8
from datetime import datetime
from flask import render_template, redirect, url_for
from app.models import RssFeeds
from .import main
from .forms import RssForm


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/rss_setting/', methods=['GET', 'POST'])
def rss_setting():
    form = RssForm()
    rssfeeds = RssFeeds.objects.all()
    if form.validate_on_submit():
        rssfeed = RssFeeds(
            rfrom=form.rfrom.data,
            rname=form.rname.data,
            rfeed=form.rfeed.data,
            rtype=form.rtype.data,
            rdate=datetime.now()
        )
        rssfeed.save()
        return redirect(url_for('.rss_setting'))
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds)



@main.route('/rss_edit/<id>', methods=['GET'])
def rss_edit(id):
    form = RssForm()
    rssfeed = RssFeeds.objects(id=id)
    rssfeeds = RssFeeds.objects.all()
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds)