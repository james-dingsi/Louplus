'''rmon.views.index'''

# 首页视图

from flask import render_template
from flask.views import MethodView

class IndexView(MethodView):
    # 通过继承MethodView实现了IndexView类
    # 当IndexView接收到GET方法的HTTP请求时，就会执行get方法
    def get(self):
        # 渲染模板
        return render_template('index.html')
