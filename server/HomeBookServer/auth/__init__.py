# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from .base import mauth
from .views import *


def init_app(app, prefix="/auth"):
    app.register_blueprint(mauth, url_prefix=prefix)
