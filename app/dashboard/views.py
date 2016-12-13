# coding=utf-8

from flask.views import MethodView
from flask import redirect, request, render_template, url_for, flash, session, jsonify
import flask.ext.login as flask_login
from app.models import AdminUser
from app.dashboard import dashboard
from app import access_log
from app.utils import md5
from flask.ext.login import login_required, current_user, login_user


@dashboard.route('/', methods=['GET'])
@login_required
def index():
    return jsonify({'login': 'success'})

class LoginInView(MethodView):
    def get(self):
        # if not current_user.is_anonymous:
        #     return redirect(url_for("dashboard.index"))
        # else:
        #     flask_login.logout_user()
        # return render_template('dashboard/login.html')
        return '''
             <form action="" method="post">
             <p><input type=text name=username>
             <p><input type=text name=password>
             <p><input type=submit value=Login>
             </input>
             <form>
             '''

    def post(self):
        name = request.form.get("username")
        pwd = request.form.get("password")
        session["username"] = name
        session["password"] = pwd
        # code = request.form.get("validcode")
        # if code != session.get("img_valid_code"):
        #     flash("验证码错误", "error")
        #     return redirect(url_for('dashboard.login'))
        access_log.info('login post test')
        try:
            access_log.info('%s %s' %(name, md5(pwd)))
            u = AdminUser.objects.get(username=name, password=md5(pwd), is_close=False)
            flask_login.login_user(u)
            return redirect(url_for('dashboard.index'))
        except AdminUser.DoesNotExist:
            access_log.info('login error')
            flash("用户名或密码错误", "error")
            return redirect(url_for('dashboard.login'))

dashboard.add_url_rule("/login", view_func=LoginInView.as_view('login'))

@dashboard.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('dashboard.login'))
    # return jsonify({'logout': 'success'})

@dashboard.route('/test')
def test_dashboard():
    access_log.info('dashboard test ok')
    return jsonify({'code': 'ok'})
