# coding=utf-8

from flask import MethodView
from flask import redirect, request, render_template, url_for, flash, session
import flask.ext.login as flask_login
from app.models import AdminUser
from app.dashboard import dashboard
from app.utils import md5
from flask.ext.login import login_required, current_user

class LoginInView(MethodView):
    def get(self):
        if not current_user.is_anonymous:
            return redirect(url_for("dashboard.index"))
        return render_template('dashboard/login.html')

    def post(self):
        name = request.form.get("username")
        pwd = request.form.get("password")
        session["username"] = name
        session["password"] = pwd
        # code = request.form.get("validcode")
        # if code != session.get("img_valid_code"):
        #     flash("验证码错误", "error")
        #     return redirect(url_for('dashboard.login'))
        try:
            u = AdminUser.objects.get(username=name, password=md5(pwd), is_removed=0)
            flask_login.login_user(u)
            return redirect(url_for('dashboard.index'))
        except AdminUser.DoesNotExist:
            flash("用户名或密码错误", "error")
            return redirect(url_for('dashboard.login'))

dashboard.add_url_rule("/login", view_func=LoginInView.as_view('login'))
