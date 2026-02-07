from .database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__="users"
    
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    password = Column(String,nullable=False)