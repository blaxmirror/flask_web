#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # 大多数情况下，响应(返回值内容)就是一个简单的字符串，作为HTML页面返回客户端
    # 如果视图函数返回的响应需要使用不同的状态码，那么可以将数字代码作为第二个返回值添加到响应文本之后
    return render_template('index.html')


# URL的可变部分只需在route修饰器中使用特殊的句法即可
# 动态部分默认使用字符串，但也可以使用类型定义，如 /user/<int:id>
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/block')
def blok():
    return render_template('extends.html')


if __name__ == '__main__':
    app.run(debug=True)
