# coding=utf-8

from app import db
from datetime import datetime as dte


class Jianshu(db.Document):
    """
    jianshu爬去的列表
    """
    url = db.StringField()
    title = db.StringField()
    author = db.StringField()
    content = db.StringField()
    meta = {
        'indexes': [
            'title',
        ],
        'collection': 'jianshu',
    }

class Student(db.Document):
    """
    测试post api
    """
    name = db.StringField()
    age = db.IntField()

class News(db.Document):
    """
    新闻
    """
    title = db.StringField(max_length=30)
    content = db.StringField()
    url = db.StringField()
    line_id = db.StringField()
    update_datetime = db.DateTimeField()
    meta = {
        'indexes': [
            'title',
        ],
        'collection': 'news',
    }

class AdminUser(db.Document):
    """
    后台管理员/客服
    """
    username = db.StringField(max_length=30)
    password = db.StringField(max_length=50)
    create_datetime = db.DateTimeField(default=dte.now)
    is_switch = db.IntField()
    yh_type = db.StringField(default="BOCB2C")
    source_include = db.ListField(default=["yhzf", "zfb"])        # 该用户处理的源站
    is_close = db.BooleanField(default=False)
    is_removed = db.IntField(default=0)

    meta = {
        "indexes": [
            "username",
            "is_switch",
            "is_removed",
        ],
    }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @property
    def is_superuser(self):
        if self.username in ['august', 'nana']:
            return True
        return False
