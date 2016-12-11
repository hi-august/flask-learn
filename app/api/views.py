# coding=utf-8

from app.api import api
from app.models import News, AdminUser
from app import access_log

from flask import Flask, jsonify, abort, make_response, request

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

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

# 需要登录权限
@auth.get_password
def get_password(username):
    if username in ['august', 'nana']:
        return 'ok'
    return None

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
def test():
    return jsonify({'code': 'ok'})

# 404处理
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    api.run(debug=True)
