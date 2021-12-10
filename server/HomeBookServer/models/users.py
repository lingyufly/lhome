# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from .db import Base
import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey

user_group = Table(
    'user_group_tab', Base.metadata,
    Column('user_id',
           Integer,
           ForeignKey('user_tab.id', ondelete='CASCADE'),
           primary_key=True),
    Column('group_id',
           Integer,
           ForeignKey('group_tab.id', ondelete='CASCADE'),
           primary_key=True))


class User(Base):
    '''
    用户信息表
    '''
    __tablename__ = 'user_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=32), unique=True, nullable=False)
    password = Column(String(length=128), nullable=False)
    photo = Column(String(length=128), nullable=True)
    create_time = Column(Integer,
                         nullable=False,
                         default=int(datetime.datetime.now().timestamp()))
    gender = Column(Integer, default=0)
    birthday = Column(Date, default=datetime.datetime.now().date())
    email = Column(String(length=128))
    mobile = Column(String(length=11))

    # groups = relationship('Group', secondary=user_group, backref='users')
    groups = relationship('Group',
                          secondary=user_group,
                          back_populates='users')


class Group(Base):
    '''
    组信息表
    '''
    __tablename__ = 'group_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=32), unique=True, nullable=False)
    create_time = Column(Integer,
                         nullable=False,
                         default=int(datetime.datetime.now().timestamp()))
    photo = Column(String(length=128), nullable=True)

    users = relationship('User', secondary=user_group, back_populates='groups')
