# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import setup_app
import os

# 启动 FLASK_SERVER=dashboard python tornado_server.py 8100
port = os.sys.argv[1]
app = setup_app()
api_server = HTTPServer(WSGIContainer(app))
api_server.listen(port)
IOLoop.instance().start()
