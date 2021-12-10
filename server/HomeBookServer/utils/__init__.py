# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

def init_app(app):
    from . import hook
    hook.init_app(app)