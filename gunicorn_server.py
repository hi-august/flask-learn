# coding=utf-8

# 启动flask应用 gunicorn -c hello:app
# flask_server=dashboard gunicorn -c gunicorn_server.py wsgi:ap
# gunicorn -w 2 -b 127.0.0.1:4000 hello:app
# gunicorn -k tornado wsgi:app -b 0.0.0.0:9000

import os

from gevent import monkey
monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '0.0.0.0:9000'
# pidfile = 'log/gunicorn.pid'
# logfile = 'log/debug.log'

#启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1
# 用monkey patch实现单进程异步响应
# todo 使用tornado实现异步响应
workers = 2
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
worker_class = 'tornado'

x_forwarded_for_header = 'X-FORWARDED-FOR'
# secure_scheme_headers = {
    # 'X-SCHEME': 'https',
# }
