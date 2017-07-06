import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'super-mega-secretkey123456789'
    SECRET_KEY = 'abc123456789fghjklmnopqwet1231543rmkadmsa'
    SECURITY_REGISTERABLE = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////sqlite/test.db'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////sqlite/therealdeal.db'


config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}

#print(basedir)
#print(SQLALCHEMY_DATABASE_URI)
#print(SQLALCHEMY_TRACK_MODIFICATIONS)
#print(SQLALCHEMY_MIGRATE_REPO)
