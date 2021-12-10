# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-10
@Description: 
'''
from .base import bill
from .wallet import *
from .account import *
from .accountbook import *
from .bill import *


def init_app(app, prefix="/bill"):
    app.register_blueprint(bill, url_prefix=prefix)
