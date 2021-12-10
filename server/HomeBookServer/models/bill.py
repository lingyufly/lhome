# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-03
@Description: 
'''

from sqlalchemy.orm import relationship
from .db import Base
import datetime
from sqlalchemy import Table, Column, Integer, Float, String, DateTime, ForeignKey


class Wallet(Base):
    '''
    用户钱包表
    '''
    __tablename__ = 'wallet_tab'
    id = Column(Integer,
                ForeignKey('user_tab.id', ondelete='CASCADE'),
                primary_key=True)
    asset = Column(Float, nullable=False, default=0.0)
    debt = Column(Float, nullable=False, default=0.0)
    lend = Column(Float, nullable=False, default=0.0)
    borrow = Column(Float, nullable=False, default=0.0)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Account(Base):
    '''
    账户表
    '''
    __tablename__ = 'account_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_tab.id', ondelete='CASCADE'))
    name = Column(String(length=32), nullable=False)
    photo = Column(String(length=128), default='')
    asset = Column(Float, nullable=False, default=0.0)
    create_time = Column(Integer,
                         nullable=False,
                         default=int(datetime.datetime.now().timestamp()))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AccountBook(Base):
    '''
    账本表
    '''
    __tablename__ = 'account_book_tab'
    id = Column(Integer,
                ForeignKey('group_tab.id', ondelete='CASCADE'),
                primary_key=True)
    category = Column(String(length=1024), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Bill(Base):
    '''
    账单表
    '''
    __tablename__ = 'bill_tab'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_tab.id', ondelete='CASCADE'))
    account_id = Column(Integer,
                        ForeignKey('account_tab.id', ondelete='CASCADE'))
    book_id = Column(Integer,
                     ForeignKey('account_book_tab.id', ondelete='CASCADE'))
    create_time = Column(Integer,
                         default=int(datetime.datetime.now().timestamp()))
    bill_type = Column(Integer)
    category = Column(Integer)
    remark = Column(Integer)
    amount = Column(Float, nullable=False)
    comment = Column(String(length=128), default='')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
