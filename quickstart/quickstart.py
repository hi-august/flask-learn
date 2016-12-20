# coding=utf-8

from flask import *

app = Flask(__name__) # 实例一个app
@app.route('/') # 路由
def index():
    return 'Index' # 返回值, 也可以返回json数据 jsonify(
@app.route('/username/')
def user():
    return 'user'
@app.route('/username/<id>')
def username(id): # 参数变量规则
    return id
@app.route('/get', methods=['GET', 'POST']) # 请求方法
def get():
    if request.method == 'POST': # 判断请求方法
        return 'POST'
    if request.method == 'GET':
        return url_for('static', filename='base.css') # 静态文件
    else:
        return 'not get or post'
# 模版系统
# 简单说就是和模板共享变量
# block定义块内容
# extends 通常加载base骨架内容
# include加载某个div具体内容
# 宏
@app.route('/template')
def template():
    username = [{'username':'tom'},{'username':'jack'}]
    return render_template('base.html', title='home', username=username)
# 重定向和404
@app.route('/error')
def error():
    return redirect(url_for('index'))
@app.errorhandler(404)
def page_not_found(error): # error常数必须存在
    return 'page not found', 404
if __name__ == '__main__':
    app.debug = True
    app.run()
