#!/usr/bin/env python
# encoding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # cache
    CACHE_TYPE= 'redis'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    CACHE_REDIS_DB = 2

    # debugtoorbar
    DEBUG_TB_HOSTS = '127.0.0.1'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail config
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'zyf6112@163.com'
    MAIL_PASSWORD = 'a123456'

    # celery config
    CELERY_BROKER_URL = 'redis://localhost:6379/10'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/11'
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_IMPORTS=("tasks")

    # sentry
    SENTRY_DSN = 'http://39aeb386bf7842a6b92dd93ff81eb998:c2085725a8b74bdfa8df0e84001c7e1e@127.0.0.1:9000/2'
    CELERY_SENTRY_DSN = ''

    # flask-sqlalchemy配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:nana@localhost/web'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # scrapyd 地址
    SCRAPYD_URLS = [
        "http://localhost:6800/schedule.json",
    ]

    # redis config
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_SETTIGNS = {
        "session": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": 9,
        },
        "order": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": 1,
        },
        "default": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": 0,
        },
    }


    MONGODB_SETTINGS = {
        'db': 'web',
        'host': 'localhost',
        'port': 27017,
    }

    # @staticmethod
    # def init_app(app):
        # app.config["flask_profiler"] = {
            # "enabled": False,
            # "storage": {
                # "engine": "mongodb",
                # "MONGO_URL": "mongodb://%s" % app.config["MONGODB_SETTINGS"]["host"],
                # "DATABASE": app.config["MONGODB_SETTINGS"]["db"],
                # "COLLECTION": "flaskprofile",
            # },
            # "basicAuth": {
                # "enabled": True,
                # "username": "admin",
                # "password": "profile"
            # }
        # }

class ApiLocalConfig(Config):
    DEBUG = True
    pass

class ApiDevConfig(Config):
    pass

class ApiProdConfig(Config):
    pass

class DashboardLocalConfig(ApiLocalConfig):
    SENTRY_DSN = 'http://3234342f940540b8b7324f2c528d0cb3:2248db2f78ab41f19b6987a7406317a9@150.129.82.175:9000/2'
    pass

class DashboardDevConfig(ApiDevConfig):
    pass

class DashboardProdConfig(ApiProdConfig):
    pass

config_mapping = {
    'api_local': ApiLocalConfig,
    'api_dev': ApiDevConfig,
    'api_prod': ApiProdConfig,

    'dashboard_local': DashboardLocalConfig,
    'dashboard_dev': DashboardDevConfig,
    'dashboard_prod': DashboardProdConfig,

    'blog_local': DashboardLocalConfig,
    'blog_dev': DashboardDevConfig,
    'blog_prod': DashboardProdConfig,
}
