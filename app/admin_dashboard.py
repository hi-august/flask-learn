# coding=utf-8

from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.login import current_user

class UserView(ModelView):
    # 只有管理员用户可见
    def is_accessible(self):
        flag = not current_user.is_anonymous
        try:
            flag = current_user.is_superuser
        except:
            flag = False
        return flag
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

