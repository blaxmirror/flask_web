#!/usr/bin/env python3

from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    # 由于很多Flask拓展都假设已经存在激活的程序上下文和请求上下文，因此必须激活程序上下文
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 线程针对send_async_email方法，args进行传参
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
