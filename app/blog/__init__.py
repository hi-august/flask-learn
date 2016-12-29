# coding=utf-8

from flask import Blueprint, request
from app import access_log

blog = Blueprint('blog', __name__,url_prefix='/blog')

import views
