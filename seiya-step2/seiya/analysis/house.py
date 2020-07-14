from sqlalchemy import func, desc, and_, select
from ..db import session, HouseModel, engine

# 热门租房小区top10   
def house_top10():
	query = session.query(
	HouseModel.house_name, 
	func.count(HouseModel.house_name).label('count')
	).group_by(HouseModel.house_name).order_by(desc('count')).limit(10)
	# query是一个查询对象，遍历后每个条目形成一个字典
	return [i._asdict() for i in query]

# 所有房源里每种户型的占比，饼图展示
def count_type():
	query = session.query(
		HouseModel.house_type,
		func.count(HouseModel.house_type).label('count')
		).group_by(HouseModel.house_type).order_by(desc('count'))
	return [i._asdict() for i in query]

# 分析所有房源的面积分布情况，以组距为10平米的直方图展示
# 数据可以生成，但是直方图搞不出来，数据不知道怎么传进去
def count_area():
	query = session.query(
		HouseModel.house_area.label('area')
		)
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['area'] = float(format(i['area'], '.1f'))
	return query_list
	
''' 这里应该还有个房龄统计，但是网站上找不到这个数据 '''

# 分析每种户型租金排名前十的小区，以折线图来展示，每户型一 条折线
# 这个统计方法没搞懂，出来的图挤成一团
def rent_top10():
	query = session.query(
		HouseModel.house_name.label('name'),
		HouseModel.house_type.label('type'),
		HouseModel.rent.label('rent')
		).group_by('name', 'type').order_by(desc('rent'))
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['rent'] = float(format(i['rent'], '.1f'))
	return query_list

'''
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