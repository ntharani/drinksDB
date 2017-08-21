""" Database Setup Routine """
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    name = Column(String(50), nullable = False)
    email = Column(String(100), nullable = False)
    picture = Column(String(100))
    id = Column(Integer, primary_key = True)


class DrinkFamily(Base):
    __tablename__ = 'drink_family'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'         : self.name,
            'id'           : self.id,
            'user_id'      : self.user_id,  
        }

class DrinkSubType(Base):
    __tablename__ = 'drink_subtype'

    name =Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    drink_family_id = Column(Integer,ForeignKey('drink_family.id', ondelete='CASCADE'))
    drink_family = relationship("DrinkFamily", backref=backref('drink_subtype', passive_deletes=True))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'user_id'      : self.user_id,  
       }


class Drink(Base):
    __tablename__ = 'drink'

    name = Column(String(100), nullable = False)
    description = Column(String(250), nullable = False)
    id = Column(Integer, primary_key = True)
    drink_subtype_id = Column(Integer,ForeignKey('drink_subtype.id', ondelete='CASCADE'))
    drink_subtype = relationship("DrinkSubType", backref=backref('drink', passive_deletes=True))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'user_id'      : self.user_id,  

       }
   


# engine = create_engine('sqlite:///drinks.db')
engine = create_engine('postgresql://catalog:udacityNagib@localhost/ndrinks')


Base.metadata.create_all(engine)
