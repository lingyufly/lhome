# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from .db import db, dbse

from .users import *


def init_app(app):
    db.init_app(app)