# coding=utf-8

from app import db
from datetime import datetime as dte
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Category(db.Document):
    name = db.StringField(required=True)

    def __unicode__(self):
        return self.name

class Post(db.Document):
    # ReferenceField保存
    # Post(title='hi', content='hello word', category=Category(name='python')).save()
    title = db.StringField(required=True)
    content = db.StringField(required=True, unique_with='title')
    create_time = db.DateTimeField(default=dte.now())
    update_time = db.DateTimeField(default=dte.now())
    tag = db.StringField()
    category = db.ReferenceField(Category, required=True)
    # commit = db.ListField()
    commit = db.ListField(field=db.ListField(field=db.StringField()))
    is_show = db.IntField(default=0)
    is_closed = db.BooleanField(default=False)
    extra_info = db.DictField()

    meta = {
        'indexes': [
            'title',
            'create_time',
            'update_time',
            'tag',
        ],
        'collection': 'blog',
    }

class Jianshu(db.Document):
    """
    jianshu爬去的列表
    primary_key
    """
    url = db.StringField(required=True)
    title = db.StringField(required=True, unique_with='url')
    link_id = db.StringField()
    author = db.StringField()
    content = db.StringField()
    category = db.ReferenceField(Category)
    catalogue = db.StringField()
    source = db.StringField()
    update_datetime = db.DateTimeField()
    create_datetime = db.DateTimeField()
    # commit = db.ListField()
    commit = db.ListField(field=db.ListField(field=db.StringField()))
    is_show = db.IntField(default=0)
    meta = {
        'indexes': [
            'title',
            'author',
            'url',
            'update_datetime',
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
    # token生成
    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    username = db.StringField(max_length=30)
    password = db.StringField(max_length=50)
    create_datetime = db.DateTimeField(default=dte.now)
    is_switch = db.IntField()
    yh_type = db.StringField(default="BOCB2C")
    source_include = db.ListField(field=db.ListField(field=db.StringField()))        # 该用户处理的源站
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

    def __unicode__(self):
        return self.username

    @property
    def is_superuser(self):
        if self.username in ['august', 'nana']:
            return True
        return False
