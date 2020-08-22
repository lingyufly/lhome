from db import db
from sqlalchemy import Column, Integer, Text


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text)
    password = Column(Text)
    age = Column(Integer)
    sex = Column(Integer)
