# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from functools import wraps
from logging import log
from flask import g

from models import dbse, User, Group
from .base import mauth
from utils.token import verify_token, create_token
from utils import make_response, logger

# login_required 装饰器
def login_required(func):
    '''装饰器，解析token数据，判断当前请求是否合法
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.token or not g.userid:
            return make_response(code=1, msg='请先登录')
        return func(*args, **kwargs)

    return wrapper


def userisgroupadmin(func):
    '''装饰器，判断当前登陆用户是否是组的管理员，

    该装饰器必须在login_required之后使用
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@mauth.route('login', methods=['POST', 'GET'])
def login():
    ''' 登陆请求
    @@@
    ### 说明
    登陆请求
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | username | string | M | 登陆用户名 |
    | password | string | M | 密码 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    username = g.args.get('username', None)
    password = g.args.get('password', None)
    if username is None or password is None:
        return make_response(code=1, msg='用户名或密码非法')

    res = dbse.query(User).filter(User.name == username).first()

    if res is None:
        return make_response(code=1, msg='用户不存在') 

    if res.name == username and res.password == password:
        token = create_token({'userid': res.id, 'username': res.name})
        return make_response(code=0, data={'token': token})
    else:
        return make_response(code=1, msg='用户名或密码错误')


@mauth.route('logout', methods=[
    'POST',
])
@login_required
def logout():
    ''' 退出登录请求
    @@@
    ### 说明
    退出登录请求
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    userid = g.userid
    if userid is None:
        return make_response(code=1, msg='用户名为空')
    return make_response(code=0, data={})
