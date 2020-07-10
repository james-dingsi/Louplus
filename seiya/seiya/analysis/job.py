from sqlalchemy import func, desc, and_, select
from ..db import session, JobModel, engine
from io import BytesIO
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def count_top10():
	'''JobModel.city:城市名称
		func.count方法查询字段的数量
		group_by将城市进行分组，order_by将字段降序排列，limit取前10条数据
	'''
	query = session.query(
		JobModel.city, 
		func.count(JobModel.city).label('count')
		).group_by(JobModel.city).order_by(desc('count')).limit(10)
	# query是一个查询对象，遍历后每个条目形成一个字典
	#print([i._asdict() for i in query])
	return [i._asdict() for i in query]
	'''
	return 返回值：
	[{'count': 33, 'city':'北京'},
	 {'count': 32, 'city':'上海'},
	 {'count': 22, 'city':'深圳'}.........] 

	'''
def salary_top10():
	''' JobModel.city:城市名称
		首先将最低工资和最高工资进行平均后，再使用func.avg查询各城市的平 均工资
		query是查询对象，需要遍历后形成字典，JSON不支持整型，要将整型转换为浮点型
	'''
	query = session.query(
		JobModel.city,
		func.avg((JobModel.salary_lower + JobModel.salary_upper)/2).label('salary')
		).group_by(JobModel.city).order_by(desc('salary')).limit(10)
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['salary'] = float(format(i['salary'], '.2f'))

	return query_list
	'''
	return 返回值：
	[{'salary': 33, 'city':'北京'},
	 {'salary': 32, 'city':'上海'},
	 {'salary': 22, 'city':'深圳'}.........] 

	'''


'''
	设置一个匿名函数
	原因是这个函数必须返回一个pandas的series类型数组，方便从蓝图文件传入模板,在页面生成表格
	如果直接将返回值设计成一个List返回，则无法实现plt输出柱状图时的坐标值调用
'''

def _hot_tags():
	# 使用pandas的read_sql方法读取数据库Job表的tags字段
	df = pd.read_sql(select([JobModel.tags]), engine)
	# 遍历df并过滤掉""和空内容，存入列表
	df_list = [i.split() for i in df.tags if i != '""']
	# 由于df_list中每项可能包含多个数据,使用pd.DataFrame将列表中的多项内容展开并拼接，重命名列名为tags
	tags_df = pd.DataFrame([i for m in df_list for i in m], columns=['tags'])
	# 使用group_by查询tags，size方法统计标签出现的数量，sort_values方法设置降序，head提取前10条
	tags_df = tags_df.groupby('tags').size().sort_values(ascending=False).head(10)
	return tags_df  
	'''
		返回一个pandas的series数组,格式为：
		tags
		移动互联网    94
		电商       78
		游戏       45
		Java     40
		教育       40
		后端       33
		运营       31
		销售       27
		企业服务     20
		移动端      20
		dtype: int64
	'''

def hot_tags():

	tags_list = []
	for i in _hot_tags().items():
		tags_list.append({'tag':i[0], 'count':i[1]})
	return tags_list
	'''
		此处返回一个列表，格式为： 
		[{'count': 94, 'tag': '移动互联网'},
		 {'count': 78, 'tag': '电商'},
		 {'count': 45, 'tag': '游戏'},
		 {'count': 40, 'tag': 'Java'},
		 {'count': 40, 'tag': '教育'},
		 {'count': 33, 'tag': '后端'},
		 {'count': 31, 'tag': '运营'},
		 {'count': 27, 'tag': '销售'},
		 {'count': 20, 'tag': '企业服务'},
		 {'count': 20, 'tag': '移动端'}]

	'''
def hot_tags_plot(format='png'):
	# 设置中文字体，如果没有Simhei字体，可以替换为其它 
	mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
	#mpl.rcParams['font.sans-serif'] = ['SimHei']
	# 避免 － 号显示为方块
	mpl.rcParams['axes.unicode_minus'] = False
	# 设置画布宽高，单位为英寸
	mpl.rcParams['figure.figsize'] = 10, 5
	# 生成柱状图
	plt.bar(_hot_tags().index, _hot_tags().values, color='orange')

	img = BytesIO()  # 实例化img，在内存中划出空间

	plt.savefig(img, format=format)  # 将img文件放入内存
	return img.getvalue()  # 返回内存中的图片数据

def experience_stat():
		
	query = session.query(
		func.concat(JobModel.experience_lower, '-', JobModel.experience_upper, '年').label('experience'),
		func.count('experience').label('count')).group_by('experience').order_by(desc('count'))
	query_list = [i._asdict() for i in query]
	return query_list


def education_stat():
	query = session.query(
		JobModel.education, 
		func.count(JobModel.education).label('count')
		).group_by('education').order_by(desc('count'))
	query_list = [i._asdict() for i in query]
	return query_list


def salary_education():
	query = session.query(
		JobModel.city,
		JobModel.education,
		func.avg((JobModel.salary_lower + JobModel.salary_upper)/2).label('salary'),
		).group_by('city', 'education').order_by(desc('city'))
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['salary'] = float(format(i['salary'], '.2f'))
	return query_list


'''
	query = session.query(
		JobModel.city,
		func.avg((JobModel.salary_lower + JobModel.salary_upper)/2).label('salary')
		).group_by(JobModel.city).order_by(desc('salary')).limit(10)
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['salary'] = float(format(i['salary'], '.2f'))
'''