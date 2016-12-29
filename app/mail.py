# -*- coding:utf-8 -*-

from flask.ext.mail import Message
from app import mail
from app import config


def send_email(subject, sender, recipients, text_body, html_body):
    # if config.DEBUG:
        # return
    # send_email(subject='good', text_body='good', sender=app.config['MAIL_USERNAME'], recipients=['1927064778@qq.com'],html_body='good')
    # 例如一些敏感词可能被屏蔽,如test
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
