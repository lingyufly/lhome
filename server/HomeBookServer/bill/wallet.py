# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-09
@Description: 钱包接口
'''

from flask import request, g
from .base import bill
from auth.wrapper import login_required, admin_required
from models import dbse, Wallet
from utils.makeresponse import make_ok_response, make_err_response, make_sqlerr_response


@bill.route('createwallet', methods=[
    'POST',
])
@login_required
def createwallet():
    ''' 创建用户钱包
    @@@
    ### 说明
    创建用户钱包，以当前登录用户的userid作为主键和外键
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    # 判断是不是已经存在该钱包
    if dbse.query(Wallet).filter(Wallet.id == g.userid).first():
        return make_err_response('钱包已经存在!')

    rcd = Wallet()
    rcd.id = g.userid
    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


@bill.route('deletewallet', methods=[
    'POST',
])
@login_required
def deletewallet():
    ''' 删除用户钱包
    @@@
    ### 说明
    删除当前登录用户的钱包信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    # 判断是不是已经存在该钱包
    rcd = dbse.query(Wallet).filter(Wallet.id == g.userid).first()
    if not rcd:
        return make_err_response('钱包不存在!')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


@bill.route('getwalletinfo', methods=[
    'POST',
])
@login_required
def getwalletinfo():
    ''' 删除用户钱包
    @@@
    ### 说明
    删除当前登录用户的钱包信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    rcd = dbse.query(Wallet).filter(Wallet.id == g.userid).first()
    if not rcd:
        return make_err_response('钱包不存在!')

    return make_ok_response(rcd.to_dict())
