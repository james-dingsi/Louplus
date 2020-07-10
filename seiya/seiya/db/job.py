from sqlalchemy import Column, Integer, String
from .base import Base

class JobModel(Base):
	__tablename__ = 'job'
	id = Column(Integer, primary_key=True)
	title = Column(String(64), unique=False, nullable=True)
	city = Column(String(16), unique=False, nullable=True)
	salary_lower = Column(Integer, nullable=True)
	salary_upper = Column(Integer, nullable=True)
	experience_lower = Column(Integer, nullable=True)
	experience_upper = Column(Integer, nullable=True)
	education = Column(String(16), nullable=True)
	tags = Column(String(256), nullable=True)
	company = Column(String(32), nullable=True)

	def __repr__(self):
		return '<Job:{}>'.format(self.title)



