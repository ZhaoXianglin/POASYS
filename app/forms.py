__author__ = 'jarvis'
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from flask.ext.mongoengine.wtf import model_form
from models import RssResults,SearchResults
class RssForm(Form):
    rfeed = StringField('rss地址')
    rfrom = StringField('rss来源')
    rname = StringField('rss名称')
    rtype = SelectField('rss类型', choices=[('新闻','新闻'),('军事','军事'),('娱乐','娱乐'),('财经', '财经'),('体育','体育'),('科技','科技'),('教育','教育'),('旅游','旅游'),('时尚','时尚')])
    rsubmit = SubmitField('保存')

SearchForm = model_form(SearchResults)


