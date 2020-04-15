#!/usr/bin/env python3
import os
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, json
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config.update(dict(SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/newsdata',
                    SQLALCHEMY_TRACK_MODIFICATIONS = False))

base = SQLAlchemy(app)


class Files(base.Model):
    __tablename__ = 'files'
    id = base.Column(base.Integer, primary_key=True, autoincrement=True)
    title = base.Column(base.String(80), unique=False, nullable=False)
    created_time = base.Column(base.DateTime, nullable=False)
    category_id = base.Column(base.Integer, base.ForeignKey('category.id'))
    content = base.Column(base.Text)
    category = base.relationship('Category', uselist=False)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time= created_time
        self.category = category
        self.content = content


class Category(base.Model):
    __tablename__ = 'category'
    id = base.Column(base.Integer, primary_key=True, autoincrement=True)
    name = base.Column(base.String(80))
    files = base.relationship('Files')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category: {}>'.format(self.name)

'''
create data
'''
content_list=[
        ['Hello Java', datetime.utcnow(), 'Java', 'File Content - Java is cool!'],
        ['Hello Python', datetime.utcnow(), 'Python', 'File Content - Python is cool!'],
        ['Hello C++', datetime.utcnow(), 'C++', 'File Content - C++ is shit!'],
        ['Hello PHP', datetime.utcnow(), 'PHP', 'File Content - PHP is not cool!']
        ]
base.drop_all()
base.create_all()
def create_data():
    for c in ['Java', 'Python', 'C++', 'PHP']:
        for i in content_list:
            name = Category(c)
            files = Files(i[0], i[1], name, i[3])
            base.session.add(name)
            base.session.add(files)
    base.session.commit()
create_data()
'''
base.create_all()

java = Category('Java')
python = Category('Python')
file1 = Files('Hello Java', datetime.utcnow(),
             java, 'File Content - Java is cool!')
file2 = Files('Hello Python', datetime.utcnow(),
             python, 'File Content - Python is cool!')
base.session.add(java)
base.session.add(python)
base.session.add(file1)
base.session.add(file2)
base.session.commit()
'''

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.route('/')
def index():
    return render_template('index.html', files=Files.query.all())

@app.route('/files/<int:file_id>')
def files(file_id):
    news = Files.query.get_or_404(file_id)

    return render_template('file.html', news=news)



if __name__ == '__main__':
    app.run()

#    base.metadata.create_all()
