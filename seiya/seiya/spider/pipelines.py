# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from flask_sqlalchemy import SQLAlchemy
from seiya.db import JobModel, session
from seiya.spider.items import JobItem

class SeiyaPipeline(object):
	def process_item(self, item, spider):
		if isinstance(item, JobItem):
			return self._process_job(item)

	def _process_job(self, item):

		session.add(JobModel(**item))

	def close_spider(self, spider):
		session.commit()
		session.close()

