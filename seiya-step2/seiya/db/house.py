from sqlalchemy import Column, Integer, String
from .base import Base

class HouseModel(Base):
	__tablename__ ='house'
	id = Column(Integer, primary_key=True)
	house_name = Column(String(64), unique=False, nullable=True)
	house_type = Column(String(64), unique=False, nullable=True)
	house_area = Column(Integer, nullable=True)
	house_age = Column(Integer, nullable=True)
	rent = Column(Integer, nullable=True)

	def __repr__(self):
		return '<House:{}>'.format(self.name)
	