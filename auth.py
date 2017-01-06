# -*- coding:utf-8 -*-

from flask import flash, jsonify, render_template, redirect, url_for
from app import login_manager
from app.models import AdminUser
from app.utils import md5
from app import config_name

# 路由配置
if "dashboard" in config_name:
    login_manager.login_view = "dashboard.login"
elif 'api' in config_name:
    login_manager.login_view = "api.create_task"

login_manager.login_message = '请登陆' # 提示信息


@login_manager.user_loader
def load_admin(username):
    try:
        u = AdminUser.objects.get(username=username)
    except AdminUser.DoesNotExist:
        return
    return u

@login_manager.unauthorized_handler
def unauthorized():
    flash('请登陆')
    return redirect(url_for('dashboard.login'))
    # return render_template('dashboard/unauthorize.html')

@login_manager.request_loader
def request_loader(request):
    token = request.headers.get('token')
    username = request.headers.get('username')
    # if token and token == TOKEN:
    if token:
        try:
            u = AdminUser.objects.get(username=username)
        except AdminUser.DoesNotExist:
            return None
        return u

    token = request.args.get("token", "")
    username = request.args.get("username")
    if token:
    # if token and token == TOKEN:
        try:
            u = AdminUser.objects.get(username=username)
        except AdminUser.DoesNotExist:
            return None
        return u

    name = request.form.get("username")
    pwd = request.form.get("password")
    if not name or not pwd:
        return
    try:
        u = AdminUser.objects.get(username=name, password=md5(pwd))
    except AdminUser.DoesNotExist:
        return None
    u.is_authenticated = True
    return u
