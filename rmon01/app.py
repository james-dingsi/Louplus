'''app.py'''
import urllib
from rmon.app import create_app
from rmon.models import db

app = create_app()

'''
使用app.cli.command装饰器，可以在项目中通过FLASK_APP=app.py flask init-db执行init_db函数，主要作用是在sqlite3数据库中创建数据库后定义数据库表
'''
@app.cli.command()
def init_db():
    # 数据库初始化
    print("sqlite3 database file is %s" % app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()

