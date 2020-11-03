from db import db
import datetime
from sqlalchemy import Table, Column, UniqueConstraint, Integer, Text, String, DateTime, Boolean, ForeignKey
# from sqlalchemy.orm import relationship


class User(db.Model):
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


class Family(db.Model):
    '''
    家庭信息表
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20), nullable=False)
    description = Column(String(length=255), nullable=False)
    createdate = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.now())
    address = Column(String(length=255), nullable=False)


class UserFamilyRelationship(db.Model):
    '''
    家庭成员信息表

    一个家庭可以包含多个成员

    一个用户可以属于多个家庭
    '''
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    familyid = Column(Integer, nullable=False)
    userisadmin = Column(Boolean)
    UniqueConstraint(userid, familyid)
