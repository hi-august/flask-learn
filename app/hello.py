#!/usr/bin/env python
# coding=utf-8

from flask import Flask

app = Flask(__name__) # 实例化一个Flask

@app.route('/') # 绑定路由
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run() # 运行本地服务器
