
from sqlalchemy.orm import sessionmaker
from faker import Faker
from alchemy import Base, engine, User, Course, Lab, Tag

# 将engine引擎作为参数创建session实例
session = sessionmaker(engine)()
# 'zh-cn'可以生成中文的伪数据内容
fake = Faker('zh-cn')

def create_users():
    for i in range(10):
        # 创建10个User类实例，伪造name和email
        user = User(name=fake.name(), email=fake.email())
        # 将实例添加到session会话中，以备提交到数据库
        # 此时的user对象没有id属性值
        # 映射类的主键字段默认从1开始自增，在传入session时自动添加该属性
        session.add(user)

def create_courses():
    # session的query方法用来查询数据，参数为映射类的类名
    # all方法表示查询全部，这里也可以省略不写
    # user就是上一个函数create_users中的user对象
    for user in session.query(User).all():
        for i in range(2):
            # 创建课程实例，name的值为8个随机汉字
            course = Course(name=''.join(fake.words(4)), user_id=user.id)
            session.add(course)

def create_labs():
    for course in session.query(Course):
        lab = Lab(name=''.join(fake.words(5)), id=course.id)
        session.add(lab)

def create_tags():
    for name in ['python', 'linux', 'java', 'mysql', 'lisp']:
        tag = Tag(name=name)
        session.add(tag)


def main():
    # 执行两个创建实例的函数，session会话内就有了这些实例
    create_users()
    create_courses()
    create_labs()
    create_tags()
    # 执行session的commit方法将全部数据提交到对应的数据表中
    session.commit()

if __name__ == '__main__':
    main()
