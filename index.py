# coding=utf-8
'''
一般导入有Flask,request,render_template
'''
from flask import Flask
from flask import *
import pdb
app = Flask(__name__)

@app.route('/hello/')
#def hello_world():pass
@app.route('/hello/<name>')
def hello(name=None):
    pdb.set_trace()
    return render_template('hello.html', name=name)

@app.route('/') # 绑定路由,即访问浏览器入口
def index():
    return 'index page' # 响应内容

@app.route('/login', methods=['GET', 'POST']) # method判断
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        return 'please login in'
        # show_the_login_form()

@app.route('/register')
def register():
    return 'register page'

@app.route('/user/')
@app.route('/user/<username>') # <username>是变量
def show_user_profile(username=None):
    tdk = {'title':'user page','keywords':'user page keywords', 'description':'user page description'}
    return render_template('user.html',username = username,tdk = tdk)

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
    app.run(host='127.0.0.2')
