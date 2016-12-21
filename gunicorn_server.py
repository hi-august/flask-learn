# coding=utf-8

# 启动flask应用 gunicorn -c hello:app
# FLASK_SERVER=dashboard gunicorn -c gunicorn_server.py wsgi:ap
# gunicorn -w 2 -b 127.0.0.1:4000 hello:app

import os

from gevent import monkey
monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '0.0.0.0:9100'
# pidfile = 'log/gunicorn.pid'
# logfile = 'log/debug.log'

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
