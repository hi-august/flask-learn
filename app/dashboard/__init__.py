# coding=utf-8

from flask import Blueprint, request
from app import access_log

dashboard = Blueprint('dashboard', __name__)

import views, auth
