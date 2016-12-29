#!/usr/bin/env python
# -*- coding:utf-8 *-*
import os
import zipfile

from app import setup_app, db
from flask.ext.script import Manager, Shell
from datetime import datetime as dte

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = setup_app()
manager = Manager(app)

# flask 中分为应用上下文和请求上下文
# 请求上下文request, session
# 应用上下文g, current_app
def make_shell_context():
    import app.models as m
    return dict(app=app, db=db, m=m)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def create_user(type):
    import getpass
    from app.models import AdminUser
    from app.utils import md5
    if type not in ["kefu", "admin"]:
        print "fail, the right command should like 'python manage.py create_user (kefu or admin)'"
        return
    username = raw_input("用户名:")
    try:
        u = AdminUser.objects.get(username=username)
        print "已存在用户, 创建失败"
        return
    except AdminUser.DoesNotExist:
        pass
    pwd1 = getpass.getpass('密码: ')
    pwd2 = getpass.getpass('确认密码: ')
    if pwd1 != pwd2:
        print "两次输入密码不一致, 创建用户失败"
        return
    u = AdminUser(username=username, password=md5(pwd1))
    if type == "kefu":
        u.is_switch = 0
    elif type == "admin":
        u.is_switch = 0

    u.save()
    print "创建用户成功"


@manager.command
def reset_password():
    import getpass
    from app.models import AdminUser
    from app.utils import md5
    username = raw_input("用户名:")
    try:
        u = AdminUser.objects.get(username=username)
        pwd1 = getpass.getpass('密码: ')
        pwd2 = getpass.getpass('确认密码: ')
        if pwd1 != pwd2:
            print "两次输入密码不一致, 重设密码失败"
            return
        u.modify(password=md5(pwd1))
        print "重设密码成功"
    except AdminUser.DoesNotExist:
        print "不存在用户", username


if __name__ == '__main__':
    manager.run()
