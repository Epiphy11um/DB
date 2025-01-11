from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# 路由
@app.route('/about')
def about():
    return 'This is the About Page.'

# 视图函数
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

# 请求对象
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    return f'Hello, {username}!'

# 响应对象
@app.route('/custom_response')
def custom_response():
    response = make_response('This is a custom response!')
    response.headers['X-Custom-Header'] = 'Value'
    return response

from flask import render_template
# 模板导入
@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)