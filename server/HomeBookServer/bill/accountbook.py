# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-09
@Description: 账本接口
'''

from flask import g
from .base import bill
from auth.wrapper import login_required
from models import dbse, AccountBook
from utils.makeresponse import make_ok_response, make_err_response, make_sqlerr_response


@bill.route('createaccountbook', methods=[
    'POST',
])
@login_required
def createaccountbook():
    ''' 创建账本账户
    @@@
    ### 说明
    创建账本账户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|用户组id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    id = g.args.get('id')
    if id is None:
        return make_err_response('用户组id不能为空!')

    rcd = dbse.query(AccountBook).filter(AccountBook.id == id).first()

    if rcd:
        return make_err_response('该用户组已经存在账本!')

    rcd = AccountBook()
    rcd.id = id
    rcd.category = ''
    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@bill.route('deleteaccountbook', methods=[
    'POST',
])
@login_required
def deleteaccountbook():
    ''' 删除账本账户
    @@@
    ### 说明
    删除账本账户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|用户组id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    id = g.args.get('id')
    if id is None:
        return make_err_response('用户组id不能为空!')

    rcd = dbse.query(AccountBook).filter(AccountBook.id == id).first()

    if not rcd:
        return make_err_response('账本不存在!')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@bill.route('getaccountbookinfo', methods=[
    'POST',
])
@login_required
def getaccountbookinfo():
    ''' 获取账本账户信息
    @@@
    ### 说明
    获取账本账户信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|用户组id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    id = g.args.get('id')
    if id is None:
        return make_err_response('用户组id不能为空!')

    rcd = dbse.query(AccountBook).filter(AccountBook.id == id).first()

    if not rcd:
        return make_err_response('账本不存在!')

    return make_ok_response(rcd.to_dict())