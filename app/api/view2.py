#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from app.api import api
from app import access_log
from flask.views import MethodView
from app.models import AdminUser, News, Student

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'web12308'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/manyue'

mongo = PyMongo(app)

class UserAPI(MethodView):

    def get(self, user_id): # 显示用户
        access_log.info('userapi ok')
        if user_id is None:
            return jsonify({'users': AdminUser.objects.filter()})
        else:
            u = AdminUser.objects.filter(username=user_id)
            return jsonify({'user': u})

    def post(self): # 添加用户
        pass

    def delete(self, user_id): # 删除用户
        pass

    def put(self, user_id): # 更新用户
        pass

# 注册url
# user_view = UserAPI.as_view('user_api')
# api.add_url_rule('/v1/users/', defaults={'user_id': None}, view_func=user_view, methods=['GET',])
# api.add_url_rule('/v1/users/', view_func=user_view, methods=['POST',])
# api.add_url_rule('/v1/users/<string:user_id>', view_func=user_view, methods=['GET', 'POST', 'PUT', 'DELETE'])

# 多个url可以用函数来注册
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "august", "age": 23}' 127.0.0.1:8000/v1/test
def register_api(view, endpoint, url, pk='id', pk_type='string'):
    view_func = view.as_view(endpoint)
    api.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    api.add_url_rule(url, view_func=view_func, methods=['POST'])
    api.add_url_rule('%s<%s:%s>' %(url, pk_type, pk), view_func=view_func, methods=['GET'])

register_api(UserAPI, 'user_api', '/v1/users/', pk='user_id')


@api.route('/v1/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return jsonify({'code': 'ok'})
    elif request.method == 'POST':
        out = request.json
        if not Student.objects.filter(name=request.json['name']):
            s = Student(name=request.json['name'], age=request.json['age'])
            s.save() # 添加
            # s.delete() # 删除
        else:
            s = Student.objects.filter(name=request.json['name'])
            for x in s:
                x.modify(age=request.json['age']) # 更新
        return jsonify({'request': out})


# pymongo接口连接
@app.route('/', methods=['GET'])
def get_lines():
    lines = mongo.db.line
    out = []
    for x in lines.find():
        out.append(x['title'])
    return jsonify({'lines': out})


if __name__ == '__main__':
    app.run(debug=True)
