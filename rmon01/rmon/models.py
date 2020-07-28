'''rmon.model'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Server(db.Model):
    '''Redis服务器类型'''
    __tablename__ = 'redis_server'
    # id属性为server对应的数据库表redis_server的主键
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):
        # 将server实例保存到数据库中
        db.session.add(self)
        db.session.commit()

    def delete(self):
        # 将server实例从数据库中删除
        db.session.delete(self)
        db.session.commit()

