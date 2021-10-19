# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from sqlalchemy.orm import relationship
from .db import Base
import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey

user_group = Table(
    'user_group_tab',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user_tab.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group_tab.id', ondelete='CASCADE'), primary_key=True))

class User(Base):
    '''
    用户信息表
    '''
    __tablename__ = 'user_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    photo = Column(String(length=255), nullable=True)
    createdate = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.now())
    gender = Column(Integer, default=0)
    birthday = Column(DateTime, default=datetime.datetime.now())
    email = Column(String(length=255))
    mobile = Column(String(length=11))

    # groups = relationship('Group', secondary=user_group, backref='users')
    groups = relationship('Group', secondary=user_group, back_populates='users')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Group(Base):
    '''
    组信息表
    '''
    __tablename__ = 'group_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20), nullable=False)
    description = Column(String(length=255), nullable=False)
    createdate = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.now())
    photo = Column(String(length=255), nullable=True)

    users = relationship('User', secondary=user_group, back_populates='groups')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

