from db import db
from sqlalchemy import Column, Integer, Text, String


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=10), nullable=False)
    password = Column(String(length=255), nullable=False)
