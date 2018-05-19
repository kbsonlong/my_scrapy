# coding:utf-8

class Config(object):
    """Base config class."""
    pass

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kbsonlong@cmdb_db:8080/cmdb2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ##解决the session is unavailable because no secret key was set.错误
    SECRET_KEY='kbsonlong2'
