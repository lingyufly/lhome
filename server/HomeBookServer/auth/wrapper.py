# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-10
@Description: 定义装饰器
'''

from functools import wraps
from flask import g
from utils.makeresponse import make_err_response


def login_required(func):
    '''装饰器，解析token数据，判断当前请求是否合法
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.token or not g.userid:
            return make_err_response('请先登录')
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    '''装饰器，判断当前登陆用户是否是组的管理员，

    该装饰器必须在login_required之后使用
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
