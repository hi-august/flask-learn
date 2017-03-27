# coding=utf-8

from app import mysql_db as db
from datetime import datetime as dte

class Test(db.Model):
    __tablename__ = 'test'
    __table_args__ = {
        'mysql_engine': 'MyISAM', # InnoDB,存储引擎
        'mysql_charset': 'utf8'
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    __table_args__ = {
        'mysql_engine': 'MyISAM', # InnoDB,存储引擎
        'mysql_charset': 'utf8'
    }
    comment_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    comment = db.relationship('Test', backref=db.backref('category_set', lazy='dynamic'))


def init_db():
    db.create_all()

def drop_db():
    db.drop_all()

def save(p):
    db.session.add(p)
    res = db.session.commit()
    return res
