# coding=utf-8

from app import setup_app, celery

app = setup_app()
app.app_context().push() # 需要导入一个app context的上下文

from task import *
