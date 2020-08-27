from db import db
import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=10), nullable=False)
    password = Column(String(length=255), nullable=False)
    createdate = Column(DateTime,
                        nullable=False,
                        default=datetime.datetime.now())
    gender = Column(Integer, default=0)
    birthday = Column(DateTime, default=datetime.datetime.now())
    email = Column(String(length=255))
    mobile = Column(String(length=11))
