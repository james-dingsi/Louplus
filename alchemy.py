from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table



engine = create_engine('mysql://root@localhost/study?charset=utf8')
# 创建声明基类时传入引擎
Base = declarative_base(engine)


class User(Base):   # 继承声明基类
    __tablename__ = 'user'     # 设置数据表名字
    id = Column(Integer, primary_key=True)  # 设置该字段为主键
    # unique设置唯一约束，nullable设置非空约束
    name = Column(String(64), unique=True, nullable=False)
    email = Column(String(64), unique=True)

    # 此特殊方法定义实例的打印样式
    def __repr__(self):
        return '<User: {}>'.format(self.name)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    # ForeigKey设置外键关联，第一个参数为字符串，user为数据表名，id为字段名
    # ondelete设置删除User实例后对关联的Course实例的处理规则
    # 'CASCADE'表示级联删除，删除用户实例后，对应的课程实例也会被删除
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    # relationship设置查询接口，以便后期进行数据库查询操作
    # 第一个参数为位置参数，参数值为外键关联的映射类名，数据类型为字符串
    # 第二个参数backref设置反向查询接口
    # backref的第一个参数'course'为查询属性，User实例使用该属性可以获得相关课程实例的列表
    # backref的第二个参数实现python语句删除用户数据时级联删除课程数据
    user = relationship('User', backref=backref('course', 
            cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Course: {}>'.format(self.name)

class Lab(Base):
    __tablename__ = 'lab'
    # 设置主键为外键，关联course表的id字段
    # 注意顺序，先定义外键，再定义主键
    id = Column(Integer, ForeignKey('course.id'), primary_key=True)
    name = Column(String(128))
    # 设置查询接口，Lab实例的course属性值为Course实例
    # Course实例的lab属性值默认为列表，列表中有一个Lab实例
    # uselist参数可以设置Course 实例的lab属性值为Lab实例而非列表
    course = relationship('Course', backref=backref('lab', uselist=False))
    
    def __repr__(self):
        return '<Lab: {}'.format(self.name)

# 创建Table类的实例，即中间表映射类，赋值给变量Rela
# 该类在实例化时，接收4个参数：
# 1、数据表名字
# 2、Base.metadata
# 3、4 两个Column(列名，数据类型，外键，主键)
Rela = Table('rela', Base.metadata,
        Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
        Column('course_id', Integer, ForeignKey('course.id'), primary_key=True))

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    # 设置查询接口，secondary指定多对多关系的中间表，注意数据类型不是字符串
    course = relationship('Course', secondary=Rela, backref='tag')

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)



if __name__ == '__main__':
    # 使用声明基类的metadata对象的create_all()方法创建数据表
    Base.metadata.create_all()
