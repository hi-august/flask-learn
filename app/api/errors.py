# coding=utf-8


from app.api import api

from flask import jsonify


@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 'Not Found', "message": "page not found", "data": ""})


@api.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({"code": '500', "message": "服务器异常", "data": ""})
