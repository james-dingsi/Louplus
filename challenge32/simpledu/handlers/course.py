from flask import Blueprint, render_template
from simpledu.models import Course, Chapter
from flask_login import login_required

# 创建蓝图，地址为 localhost:5000/course
course = Blueprint('course', __name__, url_prefix='/courses')

@course.route('/<int:course_id>')
def detail(course_id):
	course = Course.query.get_or_404(course_id)
	return render_template('course/detail.html', course=course)


@course.route('/<int:course_id>/chapters/<int:chapter_id>')
@login_required  # 章节内容需要用户登录后才能反问，所以路由要用login_required保护
def chapter(course_id, chapter_id):
	chapter = Chapter.query.get_or_404(chapter_id)
	return render_template('course/chapter.html', chapter=chapter)
	