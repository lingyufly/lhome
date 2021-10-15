#!/usr/bin/env python
# coding=utf-8
'''
    @Author: Lingyu
    @Date: 2021-10-15 08:39:22
    @LastEditTime: 2021-10-15 10:48:14
'''

from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
Base=db.Model
dbse = db.session
