# coding=utf-8

import jinja2
from flask import Blueprint, request
from app import access_log

dashboard = Blueprint('dashboard', __name__,static_folder='upload',static_url_path='/upload')

import views, auth

# 格式化时间
@jinja2.contextfilter
@dashboard.app_template_filter()
def format_datetime(context, value, format="%Y-%m-%d %H:%M:%S"):
    if not value:
        return ""
    return value.strftime(format)

# 一般用于文章简介
@jinja2.contextfilter
@dashboard.app_template_filter()
def cut_str(context, value, size=20):
    if not value:
        return value
    if len(value) < size:
        return value
    return value[:size]+"..."
