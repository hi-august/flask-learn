# coding=utf-8

from flask import Blueprint, request
from app import access_log

dashboard = Blueprint('dashboard', __name__,static_folder='upload',static_url_path='/upload')

import views, auth
