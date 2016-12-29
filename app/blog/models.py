# coding=utf-8

from app import mysql_db as db
from datetime import datetime as dte

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

    def __unicode__(self):
        return self.username


# 多对一
# 添加记录 Book(name='hi', user=User(username='august')
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # 外键的字段
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    # 不会产生字段, 会产生user方法访问外键
    # 注意User, user_set设置
    user = db.relationship('User', backref=db.backref('user_set', lazy='dynamic'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # def __init__(self, name):
        # self.name = name

    # def __repr__(self):
        # return '<Category %r>' % self.name

class Post(db.Model):
    """ 定义了五个字段，分别是 id，title，body，pub_date，category_id
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.String(20))
    # 用于外键的字段
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 外键对象，不会生成数据库实际字段
    # backref指反向引用，也就是外键Category通过backref(post_set)查询Post
    category = db.relationship('Category', backref=db.backref('post_set', lazy='dynamic'))


    # def __init__(self, title, body, category, pub_date=None):
        # self.title = title
        # self.body = body
        # if pub_date is None:
            # pub_date = time.time()
        # self.pub_date = pub_date
        # self.category = category

    # def __repr__(self):
        # return '<Post %r>' % self.title

    # def save(self):
        # db.session.add(self)
        # db.session.commit()



# class Parent(db.Model):
    # __table__ = "parent"
    # id = db.Column(db.Integer, Primary_key=True)
    # name = db.Column(db.String(50))
    # child = db.relationship("child", backref="parent")

# class Child(db.Model):
    # __table__ = "child"
    # id = db.Column(db.Integer, Primary_key=True)
    # name = db.Column(db.String(50))
    # parent_id = db.Column(db.Integer,db.ForeignKey('parent.id'))

# class Parent1(db.Model):
    # __table__ = "parent"
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(50))

# class Child1(db.Model):
    # __table__ = "child"
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(50))
    # parent_id = db.Column(db.Integer,db.ForeignKey('parent.id'))
    # parent = db.relationship("parent", backref="child")

# 用db.create_all() 创建表及其数据类型
# db.drop_all()
# 一对多
class Author(db.Model):
    # 表名
    __tablename__ = 'author'
    # Column指明字段, Integer指明类型
    # nullable不能为空
    id = db.Column(db.Integer, primary_key=True)
    is_show = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(40), index=True)
    posts = db.relationship(
        'MysqlJianshu',
        backref='Author',
    )

    def __unicode__(self):
        return self.name

class MysqlJianshu(db.Model):
    __tablename__ = 'jianshu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), index=True)
    author = db.Column(
        db.String(40),
        db.ForeignKey('author.name'),
        nullable=False,
    )
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=dte.now())


def init_db():
    db.create_all()

def drop_db():
    db.drop_all()

def save(p):
    # add_all添加列表 add()
    # Book.query.filter().delete()
    # Book.query.filter().update()
    # Book.query.filter_by().all() 返回一个列表
    # first()
    db.session.add(p)
    db.session.commit()
