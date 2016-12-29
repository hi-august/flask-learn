# coding=utf-8

from flask import Flask, request, jsonify, url_for, render_template, redirect, flash

# 定义template和static目录
# app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder = settings.STATIC_PATH)
app = Flask(__name__) # 实例一个app

# url路由, 绑定的路径一般以/结束,否则会有404错误
# 绑定了/以后,再访问/username就会跳转到/username/
@app.route('/')
def index():
    return 'Index' # 返回值, 也可以返回json数据 jsonify(

@app.route('/username/')
def user():
    return 'user'

@app.route('/username/<id>/')
def username(id): # 参数变量规则, 还支持app.route('/regex("[w]*[Ss]"):collection')))
    return id

@app.route('/get/', methods=['GET', 'POST']) # 请求方法, get/post方法
def get():
    # 获取request资源
    params = request.args
    params = request.headers
    params = request.form
    params = request.cookies
    params = request.values.to_dict()
    params = request.json # get_json()
    # 获取上传的文件
    # <input name='upload' type='file'>
    # file = request.files['the_file']
    if request.method == 'POST': # 判断请求方法
        return 'POST'
    if request.method == 'GET':
        # url_for可以为指定函数生成访问的url, 以下生成static URLs
        return url_for('static', filename='base.css') # 静态文件
    else:
        return 'not get or post'

# jinjia2
# 模版系统
# 简单说就是和模板共享变量
# block定义块内容
# extends 通常加载base骨架内容
# include加载某个div具体内容
# 宏模板类似函数, 可传递一些chanshu
# 用import加载宏模板

# 使用{# ... #}注释代码
# 使用{% set var='' %}进行赋值,{% set key,value=dosomething() %}
# 使用{{...}} 调用变量
# 使用{% if ... %}{%elif ... %}{% else %} {% endif %} 控制流程
# 使用{% for .. %}{% endfor %} 定义循环
# 使用{% block ... %}{% endblock %} 定义继承内容块
# 使用{% extends 'file' %}{% block ... %}{% endblock %} 定义模板继承的内容
# 使用{% macro input(name, value='') -%}{%- endmacro %} 定义宏模板

# 关闭模板中的转义 {{ result|safe }}

# 在模板中可以使用config,request,g和session对象,已经get_flashed_massages和url_for函数
# 在视图函数中可以使用request,g和session对象
# 也可以在jinjia2模板中注册全局变量使用
# JINJA2_GLOBALS = {'MEDIA_PREFIX': '/media/'}
# app.jinja_env.globals.update(JINJA2_GLOBALS)

@app.route('/template/')
def template():
    # flash('hello')
    # 可以在模板中用get_flashed_massages()方法拿到字符串
    username = [{'username':'tom'},{'username':'jack'}]
    # render_template用来渲染模板, 传入参数进行渲染
    # from flask import Markup
    # 转化markup
    # Markup.escape('<title> hello world </title>')
    # Markup('<em>Marked up</em>em> &raquo; HTML').striptags()
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
