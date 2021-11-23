# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
Base=db.Model
dbse = db.session
