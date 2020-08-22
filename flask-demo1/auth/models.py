from db import db
from sqlalchemy import Column, Integer, Text


class perm(db.Model):
    id = Column(Integer, primary_key=True)
    description = Column(Text)
