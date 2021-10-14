from .db import Base
import datetime
from sqlalchemy import Table, Column, UniqueConstraint, Integer, String, DateTime, Boolean, ForeignKey
# from sqlalchemy.orm import relationship

class User(Base):
    '''
    用户信息表
    '''
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

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Group(Base):
    '''
    组信息表
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20), nullable=False)
    description = Column(String(length=255), nullable=False)
    createdate = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.now())
    photo = Column(String(length=255), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserGroupRelationship(Base):
    '''
    组成员信息表

    一个组可以包含多个成员

    一个用户可以属于多个组
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    groupid = Column(Integer, nullable=False)
    userisadmin = Column(Boolean)
    UniqueConstraint(userid, groupid)
