__author__ = 'jarvis'
from flask import Blueprint

home = Blueprint('index', __name__)
rss = Blueprint('rss', __name__)
analysis = Blueprint('analysis', __name__)
search = Blueprint('search', __name__)
from .import index, rssmanage, analysis_view,search_view


