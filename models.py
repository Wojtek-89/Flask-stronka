from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    
    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
    
    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.name, self.password)
