# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-09
@Description: 账单-wallet部分接口
'''

from flask import request, g
from sqlalchemy.sql.expression import true
from sqlalchemy.util.langhelpers import walk_subclasses

import models

from .base import bill
from auth.views import login_required, userisgroupadmin
from models import dbse,User, Group,Account, AccountBook,Bill,Wallet
from utils import logger, make_response
from configs import Config


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
        return make_response(code=1, msg='钱包已经存在!')

    rcd=Wallet()
    rcd.id=g.userid
    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='执行SQL失败: {}'.format(err))
    return make_response(code=0, data={})


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
    rcd=dbse.query(Wallet).filter(Wallet.id == g.userid).first()
    if not rcd:
        return make_response(code=1, msg='钱包不存在!')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='执行SQL失败: {}'.format(err))
    return make_response(code=0, data={})


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

    rcd=dbse.query(Wallet).filter(Wallet.id == g.userid).first()
    if not rcd:
        return make_response(code=1, msg='钱包不存在!')
    
    return make_response(data=rcd.to_dict())

    