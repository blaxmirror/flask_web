#!/usr/bin/env python3

from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    # 错误：form 应为 NameForm的一个实例化对象，之前写成了form = NameForm
    form = NameForm()
    if form.validate_on_submit():
        # 查询输入数据是否在数据库中
        user = User.query.filter_by(username=form.name.data).first()
        # 若用户不存在，则将用户添加到数据库中，并设置session中known参数为False
        if user is None:
            if form.name.data != session.get('name'):
                flash('Looks like you have changed your name to %s!' % form.name.data)
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        # 重设表单数据为空
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    # 使用.get来避免未找到键的情况
    # 获取session中'known'字段，若无则默认其为False
    return render_template('index.html', name=session.get('name'),
                           form=form, known=session.get('known', False),
                           current_time=datetime.utcnow())
