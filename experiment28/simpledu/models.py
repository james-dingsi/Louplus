from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 注意这里不再传入 app 了
db = SQLAlchemy()

class Base(db.Model):
    '''所有model的一个基类，默认添加了时间戳
    '''
    # abstract设置为True表示这个类不是Model类
    __abstract__ = True
    # 设置了default和onupdate这两个时间戳就都不需要自己维护了
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 括号内从db.Model改为Base，代报把基类改为继承Base类
# 继承UserMixin类主要是为了使用flask-login中的is_authenticated方法，来判断用户是否是登录状态
class User(Base, UserMixin):
    __tablename__ = 'user'
    '''设置了三个角色，默认情况下用户注册后role为ROLE_USER
       用数值表示角色方便判断是否有权限，例如判断user.role >=ROLE_USER
       数值间的间隔为了方便以后添加其他角色
    '''
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    # 默认情况下sqlalchemy以字段名来定义列明，但这里是_password，所以明确指定列明为password
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')
    #继承了Base类后，这里不需要单独维护了
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<User:{}'.format(self.username)

    @property
    def password(self):
        '''  Python风格的getter'''
        return self._password

    @password.setter
    def password(self, orig_password):
        ''' Python风格的setter，这样设置user.password会自动为password生成哈希值并存入_password字段
        '''
        self._password = generate_password_hash(orig_password)

    
    def check_password(self, password):
        '''判断用户输入的密码和存储的哈希密码是否相等
        '''
        test = check_password_hash(self._password, password)
        print(test)
        return test

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

# 同User 改为继承Base类
class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author= db.relationship('User', uselist=False)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
