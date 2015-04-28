__author__ = 'jarvis'
from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap
from pymongo import connection
from config import config

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    #附加路由和自定义的错误页面
    '''注册蓝本'''
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
