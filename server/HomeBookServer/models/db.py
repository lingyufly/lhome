# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
dbse = db.session
Base=db.Model

def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
Base.to_dict=to_dict
