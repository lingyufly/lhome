# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from .logger import logger,getLogger
from .makeresponse import make_response
from . import hook

def init_app(app):
    hook.init_app(app)