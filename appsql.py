#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import os
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy 
from pymongo import MongoClient


app = Flask(__name__)
# 配置mysql的路径和使用的数据库
app.config.update(dict(SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/newsdata',
                    SQLALCHEMY_TRACK_MODIFICATIONS = False))

base = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).newstags    #创建mongo客户端并建库


# 调用Table方法创建多对多映射表，映射files和category两个表的id
#files_category = base.Table('files_category',
#    base.Column('files_id', base.Integer, base.ForeignKey('files.id'), primary_key=True),
#    base.Column('category_id', base.Integer, base.ForeignKey('category.id'), primary_key=True)
#    )

class Files(base.Model):
    __tablename__ = 'files'
    id = base.Column(base.Integer, primary_key=True, autoincrement=True)
    title = base.Column(base.String(80), unique=False, nullable=False)
    created_time = base.Column(base.DateTime, nullable=False)
    category_id = base.Column(base.Integer, base.ForeignKey('category.id'))
    content = base.Column(base.Text)
    # 关联映射表
    category = base.relationship('Category', uselist=False)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time= created_time
        self.category = category
        self.content = content


    def add_tag(self, tag_name):
        # 利用find_one方法查找table中files表中file_id字段
        # Mongo无须先定义表结构，等插入数据时自动会添加，所以可以先提取
        newstag = mongo.files.find_one({'files_id': self.id})
        if newstag:  # 判断newstag中是否已经存在file_id
            tag = newstag['tag']      # 如果存在，则提取对应的tag
            if tag_name not in tag:   # 判断这个tag是否在tag列表里
                tag.append(tag_name)  # 不在，则追加进tag列表
            mongo.files.update_one({'files_id': self.id}, {'$set': {'tag': tag}})
            # 利用update_one方法给files表更新一条记录
            # 如果不使用$set而直接存入，则会造成原tag列表被完全覆盖

        else:    # 如果此file_id不存在，则存入newstag一个列表结构
            tag = [tag_name]
            # 调用insert_one方法给files表添加file_id和tag两个字段
            mongo.files.insert_one({'files_id': self.id, 'tag': tag})
        return tag
        

    def remove_tag(self, tag_name):
        newstag = mongo.files.find_one({'files_id': self.id})
        if newstag:   # 判断file_id是否存在
            tag = newstag['tag']  # 存在则获取tag列表的值
            # 判断输入的tag_name是否已经存在于tag列表中
            if tag_name in tag:
                tag.remove(tag_name)   #已存在于列表则删除
                new_tag = tag   # 删除后的列表存入新表
                mongo.files.update_one({'files_id': self.id}, {
                                        '$set': {'tag': new_tag}})
                return new_tag
            else:   # 不存在则返回原列表
                return tag
        return []  # 如果对应的file_id不存在，则直接返回空列表

    @property
    def tags(self):
        newstag = mongo.files.find_one({'files_id': self.id})
        if newstag:
            return newstag['tag']
        else:
            return []


class Category(base.Model):
    __tablename__ = 'category'
    id = base.Column(base.Integer, primary_key=True, autoincrement=True)
    name = base.Column(base.String(80))
    file = base.relationship('Files')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category: {}>'.format(self.name)

'''
create data
'''


@app.route('/')
def index():
    return render_template('index.html', files=Files.query)

@app.route('/files/<int:file_id>')
def files(file_id):
    news = Files.query.get_or_404(file_id)
    return render_template('file.html', news=news, taglist=news.tags)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    base.create_all()
    java = Category('Java')
    python = Category('Python')
    linux = Category('Linux')
    php = Category('PHP')
    tech = Category('Tech')

    file1 = Files('Hello Java', datetime.utcnow(),
                 java, 'File Content - Java is cool!')
    file2 = Files('Hello Python', datetime.utcnow(),
                 python, 'File Content - Python is cool!')
    file3 = Files('Hello Linux', datetime.utcnow(), 
                linux, 'File Content - linux is well!')
    file4 = Files('Hello PHP', datetime.utcnow(), 
                php, 'File Content - PHP is not cool!')

    base.session.add_all([java, python, linux, php, tech])
    base.session.add_all([file1, file2, file3, file4])

    base.session.commit()

    file1.add_tag('Tech')
    file1.add_tag('PHP')
    file1.add_tag('Java')
    file2.add_tag('Python')
    file2.add_tag('Linux')
    file3.add_tag('Python')
    file4.add_tag('Linux')
    file4.add_tag('TEST')
