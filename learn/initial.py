from flask import Flask, make_response, redirect, abort
from flask_script import Manager

# Flask 用这个参数决定程序的根目录，以便能够找到相对于程序根目录的资源文件位置
app = Flask(__name__)
manager = Manager(app)


# 定义路由的最简单方法：利用程序实例提供的app.route装饰器来声明路由
@app.route('/')
def index():
    # 大多数情况下，响应(返回值内容)就是一个简单的字符串，作为HTML页面返回客户端
    # 如果视图函数返回的响应需要使用不同的状态码，那么可以将数字代码作为第二个返回值添加到响应文本之后
    return '<h1>Hello World</h1>'


@app.route('/response')
def mkres():
    # 可以通过返回Response对象来进一步设置响应，此处设置了cookie
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/redirect')
def redir():
    return redirect('http://www.baidu.com')


# URL的可变部分只需在route修饰器中使用特殊的句法即可
# 动态部分默认使用字符串，但也可以使用类型定义，如 /user/<int:id>
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!<h1>' % name


@app.route('/usr/id')
# abort函数用于处理错误
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name


# 启动服务器
# Flask提供的Web服务器不适合在生产环境中使用
# 使用Flask-script启动
if __name__ == '__main__':
    manager.run()
