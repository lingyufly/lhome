# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from .base import user
from .user import *
from .group import *

def init_app(app, prefix="/user"):
    app.register_blueprint(user, url_prefix=prefix)

