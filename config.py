__author__ = 'jarvis'
#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZHAOXIANGLIN'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'HOST': '202.113.78.6', 'PORT': 27017, 'DB': "POASYS"}


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}