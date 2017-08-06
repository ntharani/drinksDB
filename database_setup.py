from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class DrinkFamily(Base):
    __tablename__ = 'drink_family'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
 
class DrinkSubType(Base):
    __tablename__ = 'drink_subtype'

    name =Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    drink_family_id = Column(Integer,ForeignKey('drink_family.id'))
    drink_family = relationship(DrinkFamily)

class Drink(Base):
    __tablename__ = 'drink'

    name =Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    drink_subtype_id = Column(Integer,ForeignKey('drink_subtype.id'))
    drink_subtype = relationship(DrinkSubType)


engine = create_engine('sqlite:///drinks.db')
 

Base.metadata.create_all(engine)
