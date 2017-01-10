# coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# monkey 这里会替换原有的标准, 小心使用
# from gevent import monkey
# monkey.patch_all()
# celery任务队列, 邮件, sentry错误
from flask import Flask
from flask.ext.login import LoginManager
from flask_admin import Admin
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.cache import Cache

from config import config_mapping
import redis
import logging
from logging.handlers import SysLogHandler
from logging import Formatter, StreamHandler, FileHandler

from flask.ext.mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from redis_session import RedisSessionInterface
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True    # celery

from flask.ext.mail import Mail
mail = Mail()

db = MongoEngine()
db.connect(db='web', connect=False)
mysql_db = SQLAlchemy()

sentry = Sentry()
login_manager = LoginManager()

config_name = "%s_%s" % (os.getenv('flask_server') or 'dashboard', os.getenv('flask_config') or 'local')
config = config_mapping[config_name]

celery = Celery(__name__, broker=config.CELERY_BROKER_URL)

BASE_DIR = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

access_log = logging.getLogger('access')

def init_celery(app):
    TaskBase = celery.Task
    celery.conf.update(app.config)

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

def init_logging(app, server_type):
    fmt = Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    stdout_fhd = StreamHandler()
    stdout_fhd.setLevel(logging.INFO)
    stdout_fhd.setFormatter(fmt)
    for k, v in globals().items():
        if not k.endswith("_log"):
            continue
        logger = v
        logger.setLevel(logging.DEBUG)
        s = logger.name
        if config.DEBUG:
            f = "logs/%s.log" % s
            file_hd = FileHandler(os.path.join(BASE_DIR, f))
        else:
            mapping = {
                "order": SysLogHandler.LOG_LOCAL1,
                "line": SysLogHandler.LOG_LOCAL2,
                "common": SysLogHandler.LOG_LOCAL3,
            }
            file_hd = SysLogHandler(address=('127.0.0.1', 514), facility=mapping.get(s, SysLogHandler.LOG_LOCAL3))
        file_hd.setLevel(logging.INFO)
        file_hd.setFormatter(fmt)
        logger.addHandler(stdout_fhd)
        logger.addHandler(file_hd)

def setup_app():
    servers = {
        'api': setup_api_app,
        'dashboard': setup_dashboard_app,
        # 'blog': setup_blog_app,
    }
    server_type = config_name.split("_")[0]
    app = servers[server_type]()
    mysql_db.init_app(app)
    init_celery(app)
    from cache import cache
    cache.init_app(app)
    mail.init_app(app)
    init_logging(app, server_type)
    sentry.init_app(app, logging=True, level=logging.ERROR)
    return app

# def setup_blog_app():
    # app = Flask(__name__)
    # app.config.from_object(config)
    # # config.init_app(app)
    # print('run in blog server, use %s' %config.__name__)

    # # from blog import blog as blog_blueprint
    # db.init_app(app)
    # login_manager.init_app(app)
    # 这里作为一个蓝图导入
    # from admin import app as flask_admin_blueprint
    # app.register_blueprint(flask_admin_blueprint)
    # app.secret_key = 'A0Zr98j/3yX R~XHH]LWX/,?RT'

    # return app


def setup_dashboard_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # config.init_app(app)
    print('run in dashboard server, use %s' %config.__name__)

    db.init_app(app)
    login_manager.init_app(app)
    # 集成到dashboard, auth验证
    from app.admin_dashboard import UserView
    from app.models import AdminUser
    admin = Admin(app, 'Home')
    admin.add_view(UserView(AdminUser))
    from dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    toolbar = DebugToolbarExtension(app)
    rset = app.config["REDIS_SETTIGNS"]["session"]
    r = redis.Redis(host=rset["host"], port=rset["port"], db=rset["db"])
    app.session_interface = RedisSessionInterface(redis=r)

    return app

def setup_api_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # config.init_app(app)
    print('run in api server, use %s' %config.__name__)

    login_manager.init_app(app)
    db.init_app(app)
    from api import api as main_blueprint
    app.register_blueprint(main_blueprint)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    return app
