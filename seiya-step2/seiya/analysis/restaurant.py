from sqlalchemy import func, desc, and_, select
from ..db import session, Restaurant, engine

def evaluate_top10():
	query = session.query(
		Restaurant.name,
		Restaurant.evaluate_count.label('count')
		).group_by(Restaurant.name).order_by(desc('count')).limit(10)
	query_list = [i._asdict() for i in query]
	for i in query_list:
		i['count'] = float(format(i['count'], '.2f'))
	return query_list


