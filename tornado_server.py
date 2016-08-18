# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from index import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)  #flask默认的端口,可任意修改
IOLoop.instance().start()
