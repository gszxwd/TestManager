__author__ = 'Xu Zhao'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #database config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'default': DevConfig
}
