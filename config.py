# -*- coding: utf-8 -*-
     
import os

class Config:
    FLASK_MAIL_SUBJECT='[FLASKY]'                                                                                         
    FLASK_MAIL_SENDER='houxiangikant@163.com'
    FLASKY_ADMIN=os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_COMMIT_IN_TEARDOWN = True
    SECRET_KEY = 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass

class Developmentconfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:19930119@127.0.0.1:3306/flask'
    MAIL_SERVER ='smtp.163.com'                                                                                            
    MAIL_PORT  =25
    MAIL_USERNAME =os.environ.get('mailusername')
    MAIL_PASSWORD =os.environ.get('mailpassword')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:19930119@127.0.0.1:3306/Testing'

config = {'development':Developmentconfig,'test':TestConfig}
