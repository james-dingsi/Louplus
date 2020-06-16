from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange
from simpledu.models import db, User, Course
import re

class RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
	email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入一个邮箱地址')])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6～24个字符之间')])
	repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='重复刚才输入的密码')]) 
	job = StringField('工作 ', validators=[DataRequired()])
	role = IntegerField('角色 ', validators=[DataRequired()]) 
	submit = SubmitField('提交')

	# 使用正则表达式判断用户名输入是否仅包含数字和字符
	def validate_username(self, field):
		if not re.findall('^[0-9a-zA-Z]+$', field.data):
			raise ValidationError('请勿使用非字符和数字的用户名')
		elif User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经存在')
	
	#使用isalnum()函数判断用户名输入是否仅包含数字和字符 
	'''
	def validate_username(self, field):
		if not field.data.isalnum():
			raise ValidationError('请勿使用非字符和数字的用户名')
		elif User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经存在')
	'''		
	def validate_email(self, field):
		if User.query.filter_by(email=self.email.data).first():
			raise ValidationError('邮箱已经存在')

	''' 根据表单提交的数据创建用户 '''
	def create_user(self):
		user = User()
		user.username = self.username.data
		user.email = self.email.data
		user.password = self.password.data
		db.session.add(user)
		db.session.commit()
		return user

class LoginForm(FlaskForm):
	#email = StringField('邮箱', validators=[DataRequired(), Email()])
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
	remember_me = BooleanField('记住我')
	submit = SubmitField('提交')
	
	'''
	def validate_email(self, field):
		if field.data and not User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱未注册')
	'''
	# 如果改用用户名登录，则删掉上面的邮箱输入框，下方采用用户名验证，front.py中Login路由函数中user的值也要相应调整为通过username过滤
	def validate_username(self, field):
		if field.data and not User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名不存在')

	def validate_password(self, field):
		user = User.query.filter_by(username=self.username.data).first()
		if user and not user.check_password(field.data):
			raise ValidationError('密码错误')
	
class CourseForm(FlaskForm):
	name = StringField('课程名称', validators=[DataRequired(), Length(5, 32)])
	description = TextAreaField('课程简介', validators=[DataRequired(), Length(20, 256)])
	image_url = StringField('课程封面', validators=[DataRequired(), URL()])
	author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='作者ID不存在')])
	submit = SubmitField('提交')

	def validate_author_id(self, field):
		if not User.query.get(field.data):
			raise ValidationError('用户不存在')

	def create_course(self):
		course = Course()
		# 使用课程表单数据填充course对象
		self.populate_obj(course)
		db.session.add(course)
		db.session.commit()
		return course

	def update_course(self, course):
		self.populate_obj(course)
		db.session.add(course)
		db.session.commit()
		return course

	def delete_course(self, course):
		self.populate_obj(course)
		db.session.delete(course)
		db.session.commit()
		return course

''' 用户编辑表单 '''
class UserForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
	email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入一个邮箱地址')])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6～24个字符之间')])
	repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='重复刚才输入的密码')]) 
	job = StringField('工作 ', validators=[DataRequired()])
	role = IntegerField('角色 ', validators=[DataRequired()])  # AnyOf只允许值的范围在values列表中
	submit = SubmitField('提交')
	# 编辑用户界面仅校验用户名的合法性，不校验用户命和邮箱是否存在
	# 因为编辑后的用户名和邮箱可能已经在数据库中
	def validate_username(self, field):
		if not re.findall('^[0-9a-zA-Z]+$', field.data):
			raise ValidationError('请勿使用非字符和数字的用户名')
			
	def update_user(self, user):
		self.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		return user

	def delete_user(self, user):
		self.populate_obj(user)
		db.session.delete(user)
		db.session.commit()
		return user

	# 编辑界面创建用户时，调用RegisterForm表函数，而非UserForm
	def create_user(self):
		user = User()
		user.username = self.username.data
		user.email = self.email.data
		user.password = self.password.data
		user.job = self.job.data
		user.role = self.role.data
		db.session.add(user)
		db.session.commit()
		return user