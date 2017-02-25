#!/usr/bin/env python3

# all the import
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

# 基本设置
basedir = os.path.abspath(os.path.dirname(__file__))


# 启动app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'what the fuck'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    Bootstrap(app)
    Moment(app)
    return app


app = create_app()
db = SQLAlchemy(app)


# 定义表单类
class NameForm(Form):
    # DataRequired()验证器用来确保提交的字段不为空
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 定义Role模型和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 关系
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    # 关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return render_template('index_bootstrap.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user_bootstrap.html', name=name)


@app.route('/name', methods=['GET', 'POST'])
def namewtf():
    # 错误：form 应为 NameForm的一个实例化对象，之前写成了form = NameForm
    form = NameForm()
    if form.validate_on_submit():
        # 比较新提交的信息与原信息是否相同，如果不同使用flash提示用户
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you have changed your name!')
        # 设置一个会话，用来保存表单信息，session的使用像标准的dict一样使用
        session['name'] = form.name.data
        return redirect(url_for('namewtf'))
    # 使用.get来避免未找到键的情况
    return render_template('name_bootstrap.html', name=session.get('name'), form=form)


# name without wtf
@app.route('/namewf', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('test.html', form=form, name=name)


# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
