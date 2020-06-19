from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from simpledu.models import Course, User, Chapter
from simpledu.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required

# 创建蓝图，没有具体的url_prefix就是默认的首页('/') 
front = Blueprint('front', __name__)

@front.route('/')
def index():
	# 获取页面参数中传过来的页数
	page = request.args.get('page', default=1, type=int)
	# 生成分页对象
	pagination = Course.query.paginate(
		page=page,
		per_page=current_app.config['INDEX_PER_PAGE'],
		error_out=False
		)
	return render_template('index.html', pagination=pagination)
    #courses = Course.query.all()
    #return render_template('index.html', courses=courses)

@front.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	''' validate_on_submit是flask-wtf提供的FlaskForm的方法
	用于将表单提 交的数据和对应form中声明的表单数据验证器进行验证，返回布尔值
	''' 
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		# login_user函数的第一个参数是User对象，第二个函数是布尔值，告诉flask-login是否需要记住该用户 
		login_user(user, form.remember_me.data)
		return redirect(url_for('.index'))
	return render_template('login.html', form=form)

@front.route('/logout')
@login_required  # 退出登录功能只在用户登录状态下使用，所以用该装时期保护了这个路由处理函数，如果在未登录状态下访问此页面将被重定向到登录页面
def logout():
	logout_user()
	flash('您已经退出登录', 'success')  # flash函数向模板页面发送消息，接收消息内容和分类这两个参数
	return redirect(url_for('.index'))

@front.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		flash('注册成功，请登录', 'success')
		return redirect(url_for('.login'))
	return render_template('register.html', form=form)

