from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from simpledu.decorators import admin_required
from simpledu.models import Course, User, Live
from simpledu.forms import CourseForm, RegisterForm, UserForm, LiveForm, MessageForm
from .ws import redis
import json

# 创建后台管理页面蓝图，地址为 localhost:5000/admin
admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

''' 课程管理页 '''    
@admin.route('/courses')
@admin_required
def courses():
	page = request.args.get('page', default=1, type=int)
	pagination = Course.query.paginate(
		page=page,
		per_page=current_app.config['ADMIN_PER_PAGE'],
		error_out=False)
	return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
	form = CourseForm()
	if form.validate_on_submit():
		form.create_course()
		flash('课程创建成功', 'success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
	course = Course.query.get_or_404(course_id)
	form = CourseForm(obj=course)
	if form.validate_on_submit():
		form.update_course(course)
		flash('课程更新成功', 'success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/courses/<int:course_id>', methods=['GET', 'POST'])
@admin_required
def delete_course(course_id):
	course = Course.query.get_or_404(course_id)
	form = CourseForm(obj=course)
	form.delete_course(course)
	flash('课程删除成功', 'success')
	return redirect(url_for('admin.courses'))

''' 用户管理页面 '''
@admin.route('/users')
@admin_required
def users():
	page = request.args.get('page', default=1, type=int)
	pagination = User.query.paginate(
		page=page,
		per_page=current_app.config['ADMIN_PER_PAGE'],
		error_out=False)
	return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
	# 编辑界面创建用户时，调用RegisterForm表函数，而非UserForm
	form = RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		flash('用户创建成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_user.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
	user = User.query.get_or_404(user_id)
	form = UserForm(obj=user)
	if form.validate_on_submit():
		form.update_user(user)
		flash('用户更新成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
	user = User.query.get_or_404(user_id)
	form = UserForm(obj=user)
	form.delete_user(user)
	flash('用户删除成功', 'success')
	return redirect(url_for('admin.users'))
	

''' 直播管理页面 '''
@admin.route('/live')
@admin_required
def lives():
	page = request.args.get('page', default=1, type=int)
	pagination = Live.query.paginate(
		page=page,
		per_page=current_app.config['ADMIN_PER_PAGE'],
		error_out=False)
	return render_template('admin/lives.html', pagination=pagination)

@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
	form = LiveForm()
	if form.validate_on_submit():
		form = LiveForm()
		form.create_live()
		flash('直播创建成功', 'success')
		return redirect(url_for('admin.lives'))
	return render_template('admin/create_live.html', form=form)

@admin.route('/lives/<int:live_id>', methods=['GET', 'POST'])
@admin_required
def delete_live(live_id):
	live = Live.query.get_or_404(live_id)
	form = LiveForm(obj=live)
	form.delete_live(live)
	flash('直播删除成功', 'success')
	return redirect(url_for('admin.lives'))



@admin.route('/message', methods=['GET', 'POST'])
@admin_required
def send_message():
	form = MessageForm()
	if form.validate_on_submit():
		redis.publish('chat', json.dumps(dict(
		username='System: ',text=form.text.data)))
		flash('系统消息发送成功', 'success')
		return redirect(url_for('admin.index'))
	return render_template('admin/message.html', form=form)

