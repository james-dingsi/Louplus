from flask import Blueprint, render_template
from simpledu.models import User, Course

# 创建蓝图，地址为 localhost:5000/user
user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def user_index(username):
#	user_info = User.query.get_or_404(username)
	user_info = User.query.filter_by(username=username).first()
	'''
        user_info的返回值为sqlalchemy对象
		detail.html文件首先获取到该对象
		通过user_info.id和user_info.username方式获取用户ID和用户名
        再通过遍历user_info.publish_courses来获取列表中的课程名称
    '''
	return render_template('/user/detail.html', user_info=user_info)

