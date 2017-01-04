# coding=utf-8

from flask import Flask
from flask_admin import Admin, BaseView, expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin.contrib.sqla import ModelView as SModelView
import os.path as op
from app.models import AdminUser, Jianshu, Category, Post
# from app.blog.models import db, Author, MysqlJianshu, Post, Category, User, Book
from app import setup_blog_app
from flask.ext.login import current_user
from mongoengine import connect

DEFAULT_CONNECTION_NAME = connect('web')

# todo, auth验证, 2.外键数据管理
app = setup_blog_app()
# db.init_app(app)
# 定义程序名称
app.config['MONGODB_SETTINGS'] = {'db': 'web', 'alias':'default'}
admin = Admin(app, name='blog')

class MyView(BaseView):
    # 127.0.0.1:5000/admin
    @expose('/')
    def index(self):
        return self.render('index.html')

class PostView1(SModelView):
    pass

class AuthorView(SModelView):
    pass

class CategoryView(ModelView):
    pass

class PostView(ModelView):
    pass

class UserView(ModelView):
    # 指定过滤器
    column_filters = ['username']
    # 指定可搜索字段
    column_searchable_list = ('username',)
    # 显示的字段
    column_list = ['username', 'password', 'create_datetime']
    # 权限控制
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True
    column_editable_list = ['username', 'create_datetime']

class Jianshuview(ModelView):
    column_filters = ['title', 'author', 'source']
    column_searchable_list = ('title', 'author', 'source')
    column_list = ['title', 'source', 'author', 'link_id']
    column_editable_list = ['title', ]
    # 分页条数
    page_size = 50
    # 导出csv数据
    can_export = True
    # 修改数据样式
    create_modal = True
    edit_modal = True
    # 接受外键关联的数据
    from_ajax_refs = {
        'Category':{
            'fields': ['name'],
            'page_size': 10,
        }
    }
    inline_models = []


@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'
path = op.join(op.dirname(__file__), 'static')
# admin.add_view(FileAdmin('/Users/Augutst/stackflow/tbus/flaskdemo/app/static', '/static/', name='Static'))

admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))

admin.add_view(UserView(AdminUser))
admin.add_view(Jianshuview(Jianshu))
admin.add_view(CategoryView(Category))
admin.add_view(PostView(Post))

# admin.add_view(PostView1(Book, db.session, category='Mysql'))
# admin.add_view(PostView1(User, db.session, category='Mysql'))
# admin.add_view(PostView1(MysqlJianshu, db.session, category='Mysql'))
# admin.add_view(PostView1(Author, db.session, category='Mysql'))
# admin.add_view(PostView1(Category, db.session, category='Mysql'))
# admin.add_view(PostView1(Post, db.session, category='Mysql'))

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
