import os 
import json
from random import randint
from faker import Faker
from simpledu.models import db, User, Course, Chapter, Live

from manage import app      # new add


app.app_context().push()    # new add

fake = Faker()

def iter_users():
	yield User(
		username = 'Jack Lee',
		email = 'jack_lee@example.com',
		password = 'zxcvbnm',
		job = 'Engineer')

def iter_courses():
	author = User.query.filter_by(username='Jack Lee').first()
	with open(os.path.join(os.path.dirname(__file__), 'datas', 'courses.json')) as f:
		courses = json.load(f)
	for course in courses:
		yield Course(
			name = course['name'],
			description = course['description'],
			image_url = course['image_url'],
			author = author)

def iter_chapters():
	for course in Course.query:
		# 
		for i in range(randint(3, 10)):
			yield Chapter(
				#
				name = fake.sentence(),
				course = course,
				video_url = 'https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
				#
				video_duration = '{}:{}'.format(randint(10, 30), randint(10, 59))
				)

def iter_lives():
	yield Live(
		livename = fake.sentence(),
		live_url = '',
		liveuser_id = 1
		)

def run():
	for user in iter_users():
		db.session.add(user)

	for course in iter_courses():
		db.session.add(course)

	for chapter in iter_chapters():
		db.session.add(chapter)

	for live in iter_lives():
		db.session.add(live)
		
	try:
		db.session.commit()
	except Exception as e:
		print(e)
		db.session.rollback()

if __name__ == '__main__':
    run()
    print('ok')

