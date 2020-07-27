'''rmon.views.urls
    定义了所有API对应的URL'''

from flask import Blueprint
from views.index import IndexView

api = Blueprint('api', __name__)
# 通过api.add_url_rule方法添加了IndexView视图控制器对应的路由URL：／
# 当通过GET HTTP方法访问URL／时，就会执行IndexView中对应的get方法
api.add_url_rule('/', view_func=IndexView.as_view('index'))
