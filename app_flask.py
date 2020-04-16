#!/usr/bin/env python3
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] =True


@app.route('/<username>')
def hello(username):
	if username == 'shixiaolou':
		return 'hello {}'.format(username)
	else:
		return redirect(url_for('index'))

@app.route('/')
def index():
	course = {
		'python': 'lou+ python',
		'java': 'java base',
		'bigdata': 'spark sql',
		'teacher': 'shixiaolou',
		'is_unique': False,
		'has_tag': True,
		'tags': ['c', 'c++', 'docker']
		}
	return render_template('index.html', course=course)

@app.route('/user/<username>')
def user_index(username):
    print('User-Agent:', request.headers.get('User-Agent')) #  打印请求头数据
    print('time:', request.args.get('time')) # 获取请求 URL中？后面的time参数
    print('q:', request.args.get('q'))   # 获取请求URL中 ？后面的参数
    print('Q:', request.args.getlist('Q'))  # 当参数值不止一个时使用getlist方法
    return 'Hello {}'.format(username)

@app.route('/register', methods=['GET', 'POST'])
def register():
	print('method:', request.method)
	print('name:', request.form.get('name'))
	print('password:', request.form.get('password'))
	print('hobbies:', request.form.getlist('hobbies'))
	print('age:', request.form.get('age', default=18))
	return 'registered successfully!'

@app.route('/httptest', methods=['GET', 'POST'])
def httptest():
	if request.method == 'GET':
		print('t:', request.args.get('t'))
		print('q:', request.args.get('q'))
		return 'It is a get request!'
	elif request.method == 'POST':
		print('Q:', request.form.get('Q'))
		return 'It si a post request!'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'post {}'.format(post_id)

@app.route('/courses/<name>')
def courses(name):
	return '<h1>course: {}</h1>'.format(name)
#	return redirect(url_for('index')) #重定向到index页面
#	return render_template('courses.html', coursename=name)



@app.route('/test')
def test():
	print(url_for('index'))
	print(url_for('user_index', username='shixiaolou'))
	print(url_for('show_post', post_id=1, _external=True))
	print(url_for('show_post', post_id=2, q='python 03'))
	print(url_for('show_post', post_id=2, q='python OK'))
	print(url_for('show_post', post_id=2, _anchor='a'))
	return 'test'
	



if __name__ == '__main__':
    app.run()
