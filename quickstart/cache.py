#!/usr/bin/env python
# coding=utf-8

# 缓存可以减少服务器压力, 也可以加快访问速度
# 以下是redis作为缓存
from flask import Flask, render_template
from flask.ext.cache import Cache

app = Flask(__name__)
# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379',
    'CACHE_REDIS_DB': 2,
    })

app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'

@app.route('/')
@cache.cached(key_prefix='index')
# @cache.cached(timeout=300, key_prefix=make_cache_key, unless=None)
def hello():
    return render_template('index.html')

# 删除缓存
cache.delete(key='index')

if __name__ == '__main__':
    app.run()
