#!/usr/bin/env python
# encoding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # mail config
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '17095218904@163.com'
    MAIL_PASSWORD = 'b123456'

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

    # sentry config
    SENTRY_DSN = ""
    CELERY_SENTRY_DSN = ""

    MONGODB_SETTINGS = {
        'db': 'web12308',
        'host': 'localhost',
        'port': 27017,
    }

    @staticmethod
    def init_app(app):
        app.config["flask_profiler"] = {
            "enabled": False,
            "storage": {
                "engine": "mongodb",
                "MONGO_URL": "mongodb://%s" % app.config["MONGODB_SETTINGS"]["host"],
                "DATABASE": app.config["MONGODB_SETTINGS"]["db"],
                "COLLECTION": "flaskprofile",
            },
            "basicAuth": {
                "enabled": True,
                "username": "admin",
                "password": "profile@12308"
            }
        }

class ApiLocalConfig(Config):
    DEBUG = True
    pass

class ApiDevConfig(Config):
    DEBUG = True
    pass

class ApiProdConfig(Config):
    DEBUG = True
    pass

class AdminLocalConfig(Config):
    DEBUG = True
    pass

class AdminDevConfig(Config):
    DEBUG = True
    pass

class AdminProdConfig(Config):
    DEBUG = True
    pass

config_mapping = {
    'api_local': ApiLocalConfig,
    'api_dev': ApiDevConfig,
    'api_prod': ApiProdConfig,

    'dashboard_local': AdminLocalConfig,
    'dashboard_dev': AdminDevConfig,
    'dashboard_prod': AdminProdConfig,
}
