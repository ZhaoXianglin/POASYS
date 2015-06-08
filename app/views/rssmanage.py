# -*- coding: utf-8 -*-

from datetime import datetime
from flask.ext.mongoengine.wtf import model_form
from app.forms import RssForm
from app.models import RssResults, RssFeeds
from flask import render_template, redirect, url_for, request

__author__ = 'jarvis'
from .import rss

@rss.route('/<page>', methods=['GET', 'POST'])
def index(page=1):
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
        return redirect(url_for('.index', page=page))
    return render_template('rss_setting.html', form=form, rssfeeds=rssfeeds, pagination=pagination)


@rss.route('/delete_rssfeed/<id>', methods=['GET'])
def delete_rssfeed(id):
    item = RssFeeds(
        id=id,
    )
    item.delete()
    return redirect(url_for('.index', page=1))

@rss.route('/edit_rssfeed/', methods=['GET', 'POST'])
def edit_rssfeed():
    form = RssForm()
    if form.validate_on_submit():
        rssfeed = RssFeeds(
            id=request.form.get('itemid'),
            rfrom=form.rfrom.data,
            rname=form.rname.data,
            rfeed=form.rfeed.data,
            rtype=form.rtype.data,
            rdate=datetime.now()
        )
        rssfeed.save()
        return redirect(url_for('.index', page=1))

@rss.route('/show_content/<page>')
def show_content(page=1):
    page = int(page)
    RssResultsForm = model_form(RssResults)
    form = RssResultsForm()
    pagination = RssResults.objects.paginate(page=page, per_page=10, error_out=False)
    rssinfos = pagination.items
    return render_template('rss_show_content.html', rssinfos=rssinfos, pagination=pagination, form=form)

