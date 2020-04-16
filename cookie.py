from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cookie_index.html') #访问主页时调用模板

@app.route('/setcookie', methods = ['POST']) #cookie_index模板中指向了setcookie()函数
def setcookie():
    user = request.form['name']  #从请求中获取name字段
    req = make_response(render_template('readcookie.html'))#创建响应对象
    req.set_cookie('userID', user)  #为响应对象增加cookie
    return req   #返回cookie给浏览器
    

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome, {}</h1>'.format(name)
