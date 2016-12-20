# coding=utf-8

from flask.views import MethodView
from flask import redirect, request, render_template, url_for, flash, session, jsonify, make_response
import flask.ext.login as flask_login
from app.models import AdminUser, Jianshu
from app.dashboard import dashboard
from app import access_log
from app.utils import md5
from flask.ext.login import login_required, current_user, login_user
from mongoengine import Q
import math
import csv
import time
import StringIO

@dashboard.route('/', methods=['GET'])
def index():
    return redirect(url_for('dashboard.get_news_list'))

def parse_page_data(qs):
    total = qs.count()
    params = request.values.to_dict()
    try:
        page = int(params.get("page"))
    except TypeError:
        page = 1
    if page < 1:
        page = 1
    page_size = int(params.get("page_size", 20))
    page_num = int(math.ceil(total*1.0/page_size))
    skip = (page-1)*page_size

    cur_range = range(max(1, page-8),  min(max(1, page-8)+16, page_num+1))
    return {
        "total": total,
        "page_size": page_size,         # 每页page_size条记录
        "page_count": page_num,         # 总共有page_num页
        "cur_page": page,               # 当前页
        "previous": max(0, page-1),
        "next": min(page+1, page_num),
        "items": qs[skip: skip+page_size],
        "range": cur_range,             # 分页按钮显示的范围
    }

@dashboard.route('/news/<string:url>/edit', methods=['GET', 'POST'])
def news_edit(url):
    params = request.values.to_dict()
    queryset = dict(url__icontains=url)
    qs = Jianshu.objects(**queryset).first()
    if request.method == 'GET':
        return render_template(
            'dashboard/new_page_edit.html',
            qs=qs,

        )
    elif request.method == 'POST':
        action = params.get('edit', '')
        if action == '1':
            content = params.get('content', '')
            qs.modify(content=content)
            qs.save()
            # flash
            return redirect(url_for('dashboard.get_news_page', url=url))

@dashboard.route('/news', methods=['GET'])
@login_required
def get_news_list():
    params = request.values.to_dict()
    q = params.get("q", "")
    queryset = {}
    if q:
        queryset.update(title__icontains=q)

    action = params.get("action", "查询")

    # 导出csv
    if action == "导出csv":
        qs = Jianshu.objects.filter(**queryset)
        t1 = time.time()
        access_log.info("start export order, %s, condition:%s", current_user.username, request.values.to_dict())
        si = StringIO.StringIO()
        si.write("\xEF\xBB\xBF")
        row_header =[
            (lambda o: "%s," % o.title, "title"),
            (lambda o: "%s," % o.author, "author"),
            (lambda o: "%s," % o.url, "url"),
        ]
        cw = csv.DictWriter(si, map(lambda t: t[0], row_header))
        cw.writerow({t[0]: t[1] for t in row_header})
        info_list = []
        for o in qs:
            d = {}
            for t in row_header:
                func = t[0]
                d[func] = func(o)
            info_list.append(d)
        cw.writerows(info_list)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=%s.csv" % (time.strftime("%Y_%m_%d"))
        output.headers["Content-type"] = "text/csv"
        access_log.info("end export order, %s, time: %s", current_user.username, time.time()-t1)
        return output
    # page = int(request.args.get('page', 1))
    # if page > 1:
    #     queryset.update(page=page)
    # else:
    #     queryset.update(page=1)
    # paginate实现分页,per_page, page 搜索条件限制
    # news = Jianshu.objects.paginate(per_page=20, **queryset)
    # if news.items:
    #     return render_template(
    #         'dashboard/new_list.html',
    #         news=news,
    #         # 定制分页
    #         # page=parse_page_data(news1),
    #     )
    # else:
    #     return jsonify({'error': 1})

    # parse_page_data定制分页
    try:
        news = Jianshu.objects(**queryset)
    except:
        news = []
    if news:
        flash(params, 'info')
        return render_template(
            'dashboard/new_list1.html',
            # 定制分页
            page=parse_page_data(news),
            # 一些搜索条件, 一般可以加到value里
            condition=params,
        )
    else:
        return jsonify({'error': 1})
    # return jsonify({'login': 'success'})

@dashboard.route('/api/news', methods=['GET'])
@login_required
def get_api_news_page():
    url = request.args.get('path', '')
    if request.method == 'GET' and url:
        news = Jianshu.objects(Q(url__icontains=url)).first()
        return jsonify({'data': news})
    if 1:
        qset = {}
        news = Jianshu.objects(**qset)
        ret = parse_page_data(news)
        return jsonify({'ret': ret})

@dashboard.route('/news/<string:url>', methods=['GET', 'POST'])
@login_required
def get_news_page(url):
    news = Jianshu.objects(Q(url__icontains=url)).first()
    # return jsonify({'code': 1})
    if request.method == 'GET':
        # 用ajax加载
        return render_template('dashboard/new_page.html')
        # 直接显示在模板中
        # return render_template('dashboard/new_page.html', news=news)
    elif request.method == 'POST':
        return jsonify({'news': news})


class LoginInView(MethodView):
    def get(self):
        # if not current_user.is_anonymous:
        #     return redirect(url_for("dashboard.index"))
        # else:
        #     flask_login.logout_user()
        return render_template('dashboard/login.html')
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
            flash("登陆成功", "info")
            flask_login.login_user(u)
            return redirect(url_for('dashboard.index'))
        except AdminUser.DoesNotExist:
            access_log.info('login error')
            flash("用户名或密码错误!!!", "error")
            return redirect(url_for('dashboard.login'))

dashboard.add_url_rule("/login", view_func=LoginInView.as_view('login'))

@dashboard.route('/ajax_login', methods=['GET'])
def ajax_login():
    # ajax登陆验证
    username = request.args.get('username')
    password = request.args.get('password')
    access_log.info('username: %s password: %s' %(username, password))
    try:
        u = AdminUser.objects.get(username=username, password=password)
        if u:
            flask_login.login_user(u)
            # return redirect(url_for('dashboard.get_news_list'))
            return jsonify({'ok': 1})
    except AdminUser.DoesNotExist:
        return jsonify({'error': 1 })

@dashboard.route('/add', methods=['POST'])
def add_test():
    # 获取json数据,post ajax
    info = request.json
    access_log.info(info)
    if request.method == 'POST':
        try:
           result = int(info['a']) + int(info['b'])
           return jsonify(result=result)
        except ValueError:
            return jsonify({'error': 'You can input numbers'})

@dashboard.route('/add1', methods=['GET'])
def add_test_get():
    if request.method == 'GET':
        try:
            # 获取get方法的ajax参数
            # 类似http://127.0.0.1:8100/add1/?a=12&b=32
            a = int(request.args.get('a', 0))
            b = int(request.args.get('b', 0))
            return jsonify(result=a+b)
        except ValueError:
            return jsonify({'error': 'You can input numbers'})

@dashboard.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('dashboard.login'))
    # return jsonify({'logout': 'success'})

@dashboard.route('/test', methods=['GET', 'POST'])
def test_dashboard():
    params = request.values.to_dict()
    page = params.get('page', '')
    if page:
        pass
    return render_template('dashboard/base.html')
    # access_log.info('dashboard test ok')
    # return jsonify({'code': 'ok'})
