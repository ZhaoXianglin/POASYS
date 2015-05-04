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
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
