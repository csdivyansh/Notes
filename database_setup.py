import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')  # Default role is 'user'

    def is_admin(self):
        return self.role == 'admin'


class Note(Base):
    __tablename__ = 'Notes'

    id = Column(Integer, primary_key = True)
    title = Column(String(250), nullable = True)
    content = Column(String(10000),nullable = True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }

# class MenuItem(Base):
#     __tablename__ = 'menu_item'

#     name = Column(String(80), nullable = False)
#     id = Column(Integer, primary_key = True)
#     course = Column(String(250))
#     description = Column(String(250))
#     price = Column(String(8))
#     restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
#     restaurant = relationship(Restaurant)

    # @property
    # def serialize(self):
    #     return {
    #         'name': self.name,
    #         'description': self.description,
    #         'id': self.id,
    #         'price': self.price,
    #         'course': self.course
    #     }


engine = create_engine('sqlite:///Notes.db')
Base.metadata.create_all(engine)