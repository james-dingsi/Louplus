from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course, User, Live
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sockets import Sockets

# 该函数专门用于将flask拓展注册到app
# 将原先写在create_app函数中的db和Migrate移入此函数，再通过实例化LoginManager对象，调用init_app方法初始化app
def register_extensions(app):
    db.init_app(app)   # 实例化数据库 
    Migrate(app, db)   # 注册flask-migrate

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader  #告知flask-login如何加载用户对象
    def user_loader(id):
        return User.query.get(id)
    # 设置登录页面的路由，如果用户未登录，就会被重定向到login_view指定的页面
    login_manager.login_view = 'front.login'

def register_blueprints(app):
    from .handlers import front, course, admin, user, live, ws
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(live)
    sockets = Sockets(app)
    sockets.register_blueprint(ws)

'''app工厂函数  '''
def create_app(config):
    app = Flask(__name__)    # 创建flask对象 
    app.config.from_object(configs.get(config)) # 可以根据传入的config名称加载不同的配置
    register_extensions(app)  # 实例化LoginManager对象,用于注册flask-login
    register_blueprints(app)  #创建注册蓝图的函数 
    return app



