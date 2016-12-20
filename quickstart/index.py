# coding=utf-8
'''
一般导入有Flask,request,render_template
'''
from flask import Flask
from flask import *
from flask.ext.pymongo import PyMongo

import json
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

# mongo = PyMongo(app)
# app.config['MONGO_HOST'] = 'localhost'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'amazon'


import pymongo
conn = pymongo.MongoClient('localhost', 27017)
db = conn.amazon

# json数据


def to_json(data):
    return json.dumps(data, default=json_util.default)


@app.route('/', methods=['GET'])  # 绑定路由,即访问浏览器入口
def index():
    if request.method == 'GET':
        # lim = int(request.args.get('limit', 10))
        # off = int(request.args.get('offset'), 0)
        results = db.movie.find()  # 不可直接响应内容, 需转化
        json_results = []
        for result in results:
            json_results.append(result)
        # movies = to_json(json_results)
    return render_template('index.html',
                           movies=json_results)
    # return movies  # 响应内容


@app.route('/login', methods=['GET', 'POST'])  # method判断
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        return 'please login in'
        # show_the_login_form()


@app.route('/hello/')
#def hello_world():pass
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/register')
def register():
    return 'register page'


@app.route('/user/')
@app.route('/user/<username>')  # <username>是变量
def show_user_profile(username=None):
    tdk = {'title': 'user page', 'keywords': 'user page keywords',
           'description': 'user page description'}
    return render_template('user.html', username=username, tdk=tdk)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post id %d' % post_id


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects/')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
