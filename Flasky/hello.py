#!/usr/bin/env python3

# all the import
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from threading import Thread
import os

# 基本设置
basedir = os.path.abspath(os.path.dirname(__file__))


# 启动app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'what the fuck'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# 设定邮件主题的前缀
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[AlexFlasky]'
# 设定发件人地址
app.config['FLASKY_MAIL_SENDER'] = 'Alex Ryan <393509964@qq.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


# all the class
# 定义Role模型和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 关系
    users = db.relationship('User', backref='role', lazy='dynamic')

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


# 定义表单类
class NameForm(FlaskForm):
    # DataRequired()验证器用来确保提交的字段不为空
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 为shell命令添加上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))


# 异步发送邮件
def send_async_email(app, msg):
    # 由于很多Flask拓展都假设已经存在激活的程序上下文和请求上下文，因此必须激活程序上下文
    with app.app_context():
        mail.send(msg)


# 配置邮件发送函数
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # 线程针对send_async_email方法，args进行传参
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    # 使用.get来避免未找到键的情况
    # 获取session中'known'字段，若无则默认其为False
    return render_template('index.html', name=session.get('name'),
                           form=form, known=session.get('known', False))


# 自定义错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
