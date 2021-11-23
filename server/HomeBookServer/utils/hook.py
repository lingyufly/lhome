# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''
from utils.token import *
from flask import g
from flask.globals import request
from utils import make_response, logger

def init_app(app):
    @app.before_first_request
    def before_first_request():
        pass

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

    @app.after_request
    def after_request(response):
        return response

    @app.teardown_request
    def teardown_request(response):
        return response