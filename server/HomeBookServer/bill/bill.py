# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-09
@Description: 账单接口
'''

from flask import request, g
from .base import bill
from auth.wrapper import login_required, admin_required
from models import dbse, Bill
from utils.makeresponse import make_ok_response, make_err_response, make_sqlerr_response


@bill.route('newbill', methods=[
    'POST',
])
@login_required
def newbill():
    ''' 新建账单记录
    @@@
    ### 说明
    新建账单记录
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |account_id|integer|M|所属账户|
    |book_id|integer|M|所属账本|
    |create_time|integer|M|发生时间|
    |bill_type|integer|M|账单类型|
    |category|intger|M|分类|
    |tag|intger|M|标签|
    |amount|double|M|金额|
    |comment|string|O|备注信息|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    args = g.args
    rcd = Bill()
    rcd.user_id = g.userid
    rcd.account_id = args.get('account_id')
    rcd.book_id = args.get('book_id')
    rcd.create_time = args.get('create_time')
    rcd.bill_type = args.get('bill_type')
    rcd.category = args.get('category')
    rcd.tag = args.get('tag')
    rcd.amount = args.get('amount')
    rcd.comment = args.get('comment', '')

    if rcd.user_id is None \
        or rcd.account_id is None \
        or rcd.book_id is None \
        or rcd.create_time is None \
        or rcd.bill_type is None \
        or rcd.category is None \
        or rcd.tag is None \
        or rcd.amount is None \
        or rcd.comment is None:
        return make_err_response('提交数据错误!')

    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@bill.route('deletebill', methods=[
    'POST',
])
@login_required
def deletebill():
    ''' 删除账单记录
    @@@
    ### 说明
    删除账单记录
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|账单id|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    id = g.args.get('id')
    if id is None:
        return make_err_response('账单id不能为空!')

    rcd = dbse.query(Bill).filter(Bill.user_id == g.userid).filter(
        Bill.id == id).first()

    if not rcd:
        return make_err_response('查询不到指定账单!')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@bill.route('modifybill', methods=[
    'POST',
])
@login_required
def modifybill():
    ''' 修改账单记录
    @@@
    ### 说明
    修改账单记录
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|M|账单id|
    |create_time|integer|O|时间|
    |category|integer|O|分类|
    |tag|integer|O|标签|
    |comment|string|O|备注|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    args = g.args
    id = args.get('id')
    if id is None:
        return make_err_response('账单id不能为空!')

    rcd = dbse.query(Bill).filter(Bill.user_id == g.userid).filter(
        Bill.id == id).first()

    if not rcd:
        return make_err_response('查询不到指定账单!')

    if args.get('create_time'):
        rcd.create_time = args.get('create_time')
    if args.get('category'):
        rcd.category = args.get('category')
    if args.get('tag'):
        rcd.tag = args.get('tag')
    if args.get('comment'):
        rcd.comment = args.get('comment')

    try:
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@bill.route('querybill', methods=[
    'POST',
])
@login_required
def querybill():
    ''' 删除账单记录
    @@@
    ### 说明
    删除账单记录
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    |id|integer|O|账单id查询|
    |user_id|integer|O|用户id查询|
    |account_id|integer|O|账单id查询|
    |book_id|integer|O|账本id查询|
    |start_time|integer|O|开始时间查询|
    |end_time|integer|O|结束时间查询|
    |bill_type|integer|O|账单类型查询|
    |category|integer|O|分类查询|
    |tag|integer|O|标签查询|
    |comment|string|O|备注模糊查询|
    |page_index|string|O|分页号，缺省为1|
    |page_size|string|O|每页记录长度，缺省为100，最大为1000|

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    args = g.args
    qry = dbse.query(Bill)
    if args.get('id'):
        qry = qry.filter(Bill.id == args.get('id'))
    if args.get('user_id'):
        qry = qry.filter(Bill.user_id == args.get('user_id'))
    if args.get('account_id'):
        qry = qry.filter(Bill.account_id == args.get('account_id'))
    if args.get('book_id'):
        qry = qry.filter(Bill.book_id == args.get('book_id'))
    if args.get('bill_type'):
        qry = qry.filter(Bill.bill_type == args.get('bill_type'))
    if args.get('category'):
        qry = qry.filter(Bill.category == args.get('category'))
    if args.get('tag'):
        qry = qry.filter(Bill.tag.contains(args.get('tag')))
    if args.get('comment'):
        qry = qry.filter(Bill.comment.contains(args.get('comment')))

    if args.get('start_time') and args.get('end_time'):
        qry = qry.filter(
            Bill.create_time.between(args.get('start_time'),
                                     args.get('end_time')))

    page_index = args.get('page_index', 1)
    page_size = args.get('page_size', 100)

    if page_index <= 0 or page_size <= 0 or page_size > 1000:
        return make_err_response('分页信息输入错误!')

    try:
        rcds = qry.paginate(page=page_index,
                            per_page=page_size,
                            error_out=True)
        data = {}
        data['has_next'] = rcds.has_next
        data['page_index'] = page_index
        data['page_size'] = page_size
        data['data'] = []
        for r in rcds.items:
            data['data'].append(r.to_dict())
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response(data)
