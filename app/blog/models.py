# coding=utf-8

# http://blog.csdn.net/jmilk/article/details/53239740
# http://blog.csdn.net/u011573853/article/details/51355113
from app import mysql_db as db
from datetime import datetime as dte

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(30))

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

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '<Tag %r>' % self.name

class Post(db.Model):
    """ 定义了五个字段，分别是 id，title，body，pub_date，category_id
    """
    __tablename__ = 'post'
    __table_args__ = {
        'mysql_engine': 'MyISAM', # InnoDB,存储引擎, MyISAM类型的表强调性能,但是不支持事务
        'mysql_charset': 'utf8'
    }
    # myisam和innodb存储引擎主要区别在于,是否支持事务
    # myisam适合用于读多写,innodb适合用于事务
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', backref=db.backref('post_set', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('post_set', lazy='dynamic'))

    def __repr__(self):
        return '<Post %r>' % self.title

    def save(self):
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
    # 创建数据表
    db.create_all()

def drop_db():
    # 删除数据表
    db.drop_all()

def reset():
    # 回滚还原之前数据库状态
    db.session.rollback()

def save(p):
    # add_all添加列表,不用手动commit

    # add()
    # User.query.filter_by(username='2').order_by('username desc', 'id').group_by('username').all()
    # User.query.filter('username != 2').all()
    # User.query.filter('username like 2').offset(0).limit(5).all()

    # Book.query.filter().delete() 删除匹配到数据
    # Book.query.filter().update() b.name = 'war and peace' save(b)
    # 查询过滤器
    # filter把查询过滤器添加到原查询
    # Book.query.filter_by().all() 把等值过滤器添加到原查询, 返回一个列表
    # group_by 对结果进行分组排序
    # order_by 排序返回结果

    # all() 返回一个列表
    # first() 第一个匹配到数据,没有返回None
    # limit(2) 限制返回结果数
    # offset() 返回偏移的结果
    # get() 返回主键对应的记录
    # count() 返回匹配到结果数量
    # paginate() 返回分页对象

    # session是为了保证数据库的一致性,
    # 提交数据使用原子方式把会话对象写入数据库

    # 事务用来处理量大,复杂度高的数据
    # 数据库事务具有以下四个特性
    # 1.原子性,一个事务的所有操作,要么全部完成,要么全部不完成
    # 2. 一致性(稳定性),有非法数据(外键约束),事务返回
    # 3. 隔离性,事务独立运行,一个事务如果影响到其他事务,其他事务会撤回
    # 4. 持久性,软硬件崩溃,innodb会根据日志进行重构修改

    # inner join, left join, right join
    # left join(左连接),以左边的表为主,左边表全部列出,右表分为以下三种,
    # 1.右表有一条,会返回新的一条记录
    # 2.右表有n条记录,会返回n条新的记录
    # 3.右表没有可以null列出
    # right join(右连接),右边的表全部列出,左表分以下三种情况,
    # 1.左表有一条记录,会返回新的一条记录
    # 2.左表有n条记录,会返回新的n条记录
    # 3.左表没有记录,可以用null填充
    # inner join(内连接)(join), 相当于交集
    # 左表和右表都匹配到返回
    # full join(完全连接), 相当于并集
    # 左表或右表匹配到都返回

    # 高并发下可以加锁,以免数据冲突
    # u = User.query.with_lockmode('update').filter_by(username='august').first()
    # u.query.update({'username': 'h1'})

    try:
        db.session.add(p)
    except Exception as e:
        print(e)
        db.session.rollback()
    else:
        db.session.commit()
