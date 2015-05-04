__author__ = 'jarvis'
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators
class RssForm(Form):
    rfeed = StringField('rss地址')
    rfrom = StringField('rss来源')
    rname = StringField('rss名称')
    rtype = SelectField('rss类型', choices=[('新闻','新闻'),('娱乐','娱乐'),('财经','财经'),('证券','证券')])
    rsubmit = SubmitField('保存')