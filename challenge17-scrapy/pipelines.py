# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from git.models import Repository, engine
from git.items import GitItem


class GitPipeline(object):
	def process_item(self, item, spider):
		
		item['update_time'] = datetime.strptime(item['update_time'].replace('T',' ').rstrip('Z'), '%Y-%m-%d %H:%M:%S')

		self.session.add(Repository(**item))
		return item

	def open_spider(self, spider):
		'''在爬虫被开启时，创建数据库session
		'''
		Session = sessionmaker(bind=engine)
		self.session = Session()

	def close_spider(self, spider):
		'''在爬虫被关闭后，提交session，然后关闭session
		'''
		self.session.commit()
		self.session.close()

