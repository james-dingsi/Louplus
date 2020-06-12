class BaseConfig(object):
    SECRET_KEY = 'makesure to set a very secret key'
    INDEX_PER_PAGE = 9  # 设置首页默认每页显示9个课程
    ADMIN_PER_PAGE = 15 # 设置管理页每页显示15个条目
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/simpledu?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

