from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError 
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User
import re

class RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
	email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入一个邮箱地址')])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6～24个字符之间')])
	repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='重复刚才输入的密码')]) 
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
	
