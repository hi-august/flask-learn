# coding=utf-8

from app.api import api
from app.models import News, AdminUser, Jianshu
from app import access_log
from app.utils import md5
import math

from flask import Flask, jsonify, abort, make_response, request, g
from flask.ext.login import login_required

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# 验证密码
@auth.verify_password
def verify_password(username_or_token, password):
    try:
        user = AdminUser.objects(username=username_or_token).first()
        if user.password == md5(password):
            # 存储g.user
            # g.user = user.username
            return True
        return False
    except:
        return False

# 需要登录权限
# @auth.get_password
# def get_password(username):
    # user = AdminUser.objects(username=username).first()
    # print username, user.password
    # if user:
        # return user.password
    # return None

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

@api.route('/users', methods=['GET'])
def get_users():
    access_log.info('users ok')
    out = []
    for x in AdminUser.objects.filter():
        out.append(x['username'])
    return jsonify({'users': out})

@api.route('/news', methods=['GET'])
def get_news():
    access_log.info('news ok')
    out = []
    for x in News.objects.filter()[:10]:
        out.append({x['title']: x['url']})
    return jsonify({'news': out})


@auth.error_handler
def unauthorized():
    access_log.info('[Unauthorized]')
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


tasks = [
    {
            'id': 1,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
    {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web',
            'done': False
        }
]

# curl -i 127.0.0.1:5000/api/tasks/2
# curl -u august:ok 127.0.0.1:5000/api/2 简单验证
@api.route('/api/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_tasks(task_id):
    access_log.info('ok')
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task})

# @app.route('/api/tasks', methods=['GET'])
# def get_task():
#     return jsonify({'tasks': tasks})

# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/api/tasks}'
@api.route('/api/tasks', methods=['POST', 'GET'])
@auth.login_required

# flask_login实现
# @login_required
def create_task():
    if request.method == 'GET':
        return jsonify({'tasks': tasks})

    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@api.route('/test', methods=['GET'])
@auth.login_required
def test():
    return jsonify({'code': 'ok'})

@api.route('/api/v1/check', methods=['GET'])
@auth.login_required
def check():
    realip = request.environ['REMOTE_ADDR']
    access_log.info('[check ok ip: %s]'%realip)
    # 分页
    # posts = Jianshu.objects()
    # ret = parse_page_data(posts)
    return jsonify({
        'code': 1,
        'message': 'ok',
        # 'data': ret,
    })
# 404处理
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    api.run(debug=True)
