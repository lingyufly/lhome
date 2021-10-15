#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-10-15 08:39:22
    @LastEditTime: 2021-10-15 17:36:30
'''

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
Base=db.Model
dbse = db.session
