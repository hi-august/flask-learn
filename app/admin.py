# coding=utf-8

from flask import Flask
from flask_admin import Admin, BaseView, expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin.contrib.sqla import ModelView as SModelView
# import os.path as op
from app.models import AdminUser, Jianshu, Category, Post
from flask.ext.login import current_user
from flask import Blueprint

# flask_admin拓展为一个蓝图
# 这种方式需要权限重新验证
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

class AdminBlueprint(Blueprint):
    views=None


    def __init__(self,*args, **kargs):
        self.views = []
        return super(AdminBlueprint, self).__init__('admin2', __name__,url_prefix='/admin2',static_folder='static', static_url_path='/static/admin')


    def add_view(self, view):
        self.views.append(view)

    def register(self,app, options, first_registration=False):
        print app
        admin = Admin(app, name='blog')

        for v in self.views:
            admin.add_view(v)

        return super(AdminBlueprint, self).register(app, options, first_registration)

app = AdminBlueprint('admin2', __name__,url_prefix='/admin2',static_folder='static', static_url_path='/static/admin')
app.add_view(UserView(AdminUser))

