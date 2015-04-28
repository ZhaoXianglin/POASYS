__author__ = 'jarvis'
import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZHAOXIANGLIN'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_SERVER = '202.113.78.6'
    MONGO_PORT = 27017
    MONGO_DB = 'POASYS'


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}