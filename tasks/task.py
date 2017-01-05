# coding=utf-8

# celery -A task worker --loglevel=info
from . import celery
from app.mail import send_email
from flask import current_app


ADMINS = ['1927064778@qq.com']

# done 提示RuntimeError: working outside of application context
# 导入一个app context

@celery.task(bind=True, ignore_result=True)
def async_send_email(self, subject, body):
    # app = current_app._get_current_object()
    # with app.app_context():
    send_email(subject,
               current_app.config["MAIL_USERNAME"],
               ADMINS,
               "",
               body)
