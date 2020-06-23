from git.models import Repository, session
from git.items import GitItem


class GitPipeline(object):
	def process_item(self, item, spider):
		session.add(Repository(**item))
		'''
		# mysql库可以根据表结构类型自动将写入库的数据进行格式匹配，所以，此部分格式转化可以省略
		item['update_time'] = datetime.strptime(item['update_time'], 
			'%Y-%m-%dT%H:%M:%SZ')
		if item.get('commits'):     
			item['commits'] = int(item['commits'].replace(',', ''))
			item['branches'] = int(item['branches'])
			item['releases'] = int(item['releases'])
		# 删除千分位逗号的语句可以在爬虫文件中书写，以提高效率
		if item.get('commits'):     
			item['commits'] = item['commits'].replace(',', '')
		'''
		return item

	def close_spider(self, spider):
		session.commit()
		session.close()
