# coding=utf-8

from app import mysql_db as db
from datetime import datetime as dte

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % self.username


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

    def to_json(self):
        return {
            'name': self.name,
            'user': self.user,
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    pub_date = db.Column(db.DateTime, default=dte.now())

    def __repr__(self):
        return '<Comment %r>' % self.name

class Post(db.Model):
    """ 定义了五个字段，分别是 id，title，body，pub_date，category_id
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=dte.now())
    # 用于外键的字段
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 外键对象，不会生成数据库实际字段
    # backref指反向引用，也就是外键Category通过backref(post_set)查询Post
    category = db.relationship('Category', backref=db.backref('post_set', lazy='dynamic'))

    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    comment = db.relationship('Comment', backref=db.backref('post_set', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('post_set', lazy='dynamic'))

    def __repr__(self):
        return '<Post %r>' % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()


    def modify(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'pub_date': self.pub_date,
            'category': self.category,
            'user': self.user,
            'comment': self.comment,
        }



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
    #  posts = db.relationship(
        #  'MysqlJianshu',
        #  backref='Author',
    #  )

    def __unicode__(self):
        return self.name

class MysqlJianshu(db.Model):
    __tablename__ = 'jianshu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    url = db.Column(db.String(200), index=True)
    link_id = db.Column(db.String(32), index=True)
    #  author = db.Column(
        #  db.String(40),
        #  db.ForeignKey('author.name'),
        #  nullable=False,
    #  )
    content = db.Column(db.Text)
    update_datetime = db.Column(db.DateTime, default=dte.now())


def init_db():
    db.create_all()

def drop_db():
    db.drop_all()

def save(p):
    # add_all添加列表 add()
    # Book.query.filter().delete()
    # Book.query.filter().update() b.name = 'war and peace' save(b)
    # Book.query.filter_by().all() 返回一个列表
    # first()
    db.session.add(p)
    res = db.session.commit()
    return res
