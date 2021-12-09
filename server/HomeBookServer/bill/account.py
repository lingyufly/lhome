# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-09
@Description: 账户管理
'''

from flask import request, g
from .base import bill
from auth.views import login_required, userisgroupadmin
from models import dbse, User, Group, Account, AccountBook, Bill, Wallet
from utils import logger, make_response, makeresponse
from configs import Config


@bill.route('createaccount', methods=[
    'POST',
])
@login_required
def createaccount():
    ''' 创建用户钱包账户
    @@@
    ### 说明
    创建用户钱包账户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |name|string|M|账户名称|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    name = g.args.get('name', None)
    if not name:
        return make_response(code=1, msg='账户名不可为空')

    rcd = Account()
    rcd.user_id = g.userid
    rcd.name = name

    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='执行SQL失败: {}'.format(err))
    return make_response(code=0, data={})


@bill.route('deleteaccount', methods=[
    'POST',
])
@login_required
def deleteaccount():
    ''' 删除用户钱包账户
    @@@
    ### 说明
    删除用户钱包账户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|账户id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    id = g.args.get('id', None)
    if id is None:
        return make_response(code=1, msg='待删除的账户id错误')

    rcd = dbse.query(Account).filter(Account.id == id).first()
    if rcd is None:
        return make_response(code=1, msg='账户不存在')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='执行SQL失败: {}'.format(err))

    return make_response(code=0)


@bill.route('getaccountinfo', methods=[
    'POST',
])
@login_required
def getaccountinfo():
    ''' 获取用户钱包账户信息
    @@@
    ### 说明
    获取用户钱包账户信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|O|账户id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    rcds = []
    id = g.args.get('id', None)
    if id is None:
        # 不指定id时查询用户的全部账户信息
        rcds = dbse.query(Account).filter(Account.user_id == g.userid).all()
    else:
        rcds = dbse.query(Account).filter(Account.id == id).all()

    if id is not None and len(rcds) == 0:
        return make_response(code=1, msg='查询不到指定账户信息!')

    data = []
    for r in rcds:
        data.append(r.to_dict())

    return make_response(data=data)