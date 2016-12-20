# coding:utf-8

from flask import Flask
from flask import *
app = Flask(__name__)

@app.route('/')
def test():
    return 'index page'
@app.route('/template')
def template():
    user = {'username': 'lucy'} # 传递到模版内容
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('template.html',\
    posts = posts,\
    title = 'home',user = user) # 加载模版

if __name__ == '__main__':
    app.debug = True
    app.run()
