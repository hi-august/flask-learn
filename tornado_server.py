# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import setup_app
import os

# 启动 flask_server=dashboard python tornado_server.py 8100
port = os.sys.argv[1]
app = setup_app()
api_server = HTTPServer(WSGIContainer(app))
# 监听端口,绑定socket事件
api_server.bind(port)
# 开启4个进程
api_server.start(2)
IOLoop.current().start()
