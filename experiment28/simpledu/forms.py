from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError 
from wtforms.validators import Length, Email, EqualTo, DataRequired
from simpledu.models import db, User

class RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
	email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入一个邮箱地址')])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6～24个字符之间')])
	repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='重复刚才输入的密码')]) 
	submit = SubmitField('提交')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经存在')

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
	email = StringField('邮箱', validators=[DataRequired(), Email()])
	#username = StringField('username', validators=[DataRequired()])
	password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
	remember_me = BooleanField('记住我')
	submit = SubmitField('提交')
	#def validate_username(self, field):

	def validate_email(self, field):
		if field.data and not User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱未注册')

	def validate_password(self, field):
		user = User.query.filter_by(email=self.email.data).first()
		print(user)
		print(field.data)
		if user and not user.check_password(field.data):
			raise ValidationError('密码错误')
	
