from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	score = Column(Integer)
	evaluate_count = Column(Float(3,2))
	per_capita = Column(Integer)
	sort = Column(String(64))
	place = Column(String(64))
	flavor = Column(String(64))
	environment = Column(String(64))
	service = Column(String(64))

	def __repr__(self):
		return '<Restaurant:{}>'.format(self.name)
