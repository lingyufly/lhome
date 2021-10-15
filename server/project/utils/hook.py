#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-10-15 10:55:32
    @LastEditTime: 2021-10-15 16:08:04
'''
from utils.token import *
from flask import g
from flask.globals import request
from utils import make_response, logger

def hook_init(app):
    @app.before_request
    def before_request():
        # 解析token
        g.userid=None
        g.token=None
        try:
            if request and request.headers and 'token' in request.headers:
                tokenStr=request.headers['token']
                g.token=verify_token(tokenStr)
                if g.token is not None:
                    g.userid=g.token.get('userid')
            
        except Exception as err:
            return make_response(code=1, msg='解析token失败 {}'.format(err))

        # 解析传入参数
        data={}
        if request.args:
            data.update(request.args)
        if request.form:
            data.update(request.form)
        if request.json:
            data.update(request.json)
        g.args=data
