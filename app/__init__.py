__author__ = 'jarvis'
# coding:utf-8
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from config import config

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = MongoEngine()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    #注册蓝图
    from .views import home, rss, analysis, search

    #app.register_blueprint(main_blueprint, url_profix='/main')
    app.register_blueprint(home)
    app.register_blueprint(rss, url_prefix='/rssmanage')
    app.register_blueprint(analysis, url_prefix='/analysis')
    app.register_blueprint(search, url_prefix='/search')
    return app
