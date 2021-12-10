# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 组信息注册、删除、修改和查询功能。
'''

from .base import user
from flask import g
from auth.wrapper import login_required, admin_required
from models import dbse, User, Group
from utils.makeresponse import make_ok_response, make_err_response, make_sqlerr_response


def groupnameValid(groupname):
    rcd = dbse.query(Group).filter(Group.name == groupname).first()
    return False if rcd else True


@user.route('checkgroupname', methods=[
    'POST',
])
def checkgroupname():
    '''检查组名是否冲突
    @@@
    ### 说明
    检查组名是否冲突
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupname | string | M | 组名 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args
    groupname = args.get('groupname', None)
    if groupname is None:
        return make_err_response('组名不能为空!')

    if not groupnameValid(groupname):
        return make_err_response('组名不可用!')
    else:
        return make_ok_response()


@user.route('registergroup', methods=[
    'POST',
])
@login_required
def registergroup():
    '''注册组
    @@@
    ### 说明
    注册组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupname | string | M | 组名 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    userid = g.userid
    args = g.args

    groupname = args.get('groupname', None)

    if not groupname:
        return make_err_response('组名不能为空!')

    if not groupnameValid(groupname):
        return make_err_response('组名不可用!')

    groupRcd = Group()
    groupRcd.name = groupname

    groupRcd.users = [dbse.query(User).filter(User.id == userid).first()]

    try:
        dbse.add(groupRcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


@user.route('deletegroup', methods=[
    'POST',
])
@login_required
@admin_required
def deletegroup():
    '''删除组
    @@@
    ### 说明
    删除组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | int | M | 组id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    groupid = g.args.get('groupid')
    rcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not rcd:
        return make_err_response('组不存在')

    rcd = dbse.query(Group).filter(Group.id == groupid).first()
    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


@user.route('modifygroup', methods=[
    'POST',
])
@login_required
@admin_required
def modifygroup():
    '''修改组信息
    @@@
    ### 说明
    修改组信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | int | M | 组id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args
    groupid = args.get('groupid')
    if groupid is None:
        return make_err_response('组id不能为空!')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return make_err_response('组不存在!')

    if args.get('groupname', None):
        groupRcd.name = args.get('groupname', None)

    try:
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@user.route('getgroupinfo', methods=[
    'POST',
])
@login_required
def getgroupinfo():
    '''根据组id查询组信息
    @@@
    ### 说明
    根据组id查询组信息

    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    groupid = g.args.get('groupid', None)
    if groupid is None:
        return make_err_response('组id不能为空!')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return make_err_response('组不存在!')

    data = groupRcd.to_dict()
    data["users"] = []
    for user in groupRcd.users:
        data['users'].append(user.to_dict())
    return make_ok_response(data)


@user.route('inviteuser', methods=[
    'POST',
])
@login_required
@admin_required
def inviteuser():
    ''' 邀请用户进组
    @@@
    ### 说明
    邀请用户进组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |
    | userid | integer | M | 被邀请用户id |
    | isadmin | bool | O | 新用户是否作为管理员 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
        
    '''
    args = g.args
    groupid = args.get('groupid')
    userid = args.get('userid')
    isadmin = args.get('isadmin', False)

    if groupid is None or userid is None:
        return make_err_response('组id和用户id不能为空!')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    grpRcd = dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd is None or grpRcd is None:
        return make_err_response('用户或组信息错误!')

    if userRcd in grpRcd.users:
        return make_err_response('用户已经在该组中!')

    grpRcd.users.append(userRcd)

    try:
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@user.route('removeuser', methods=[
    'POST',
])
@login_required
@admin_required
def removeuser():
    '''从组中删除用户
    @@@
    ### 说明
    从组中删除用户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |
    | userid | integer | M | 被删除用户id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args
    groupid = args.get('groupid')
    userid = args.get('userid')

    if groupid is None or userid is None:
        return make_err_response('!')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    grpRcd = dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd is None or grpRcd is None:
        return make_err_response('用户或组信息错误!')

    if userRcd not in grpRcd.users:
        return make_err_response('用户不存在当前组中，无法删除!')

    try:
        grpRcd.users.remove(userRcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@user.route('joingroup', methods=[
    'POST',
])
@login_required
def joingroup():
    '''加入组

    @@@
    ### 说明
    加入组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    
    '''
    userid = g.userid
    groupid = g.args.get('groupid', None)
    if not groupid:
        return make_err_response('组id不能为空!')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    grpRcd = dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd in grpRcd.users:
        return make_err_response('已经加入该组，不需要重复加入!')

    try:
        grpRcd.users.append(userRcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


@user.route('leavegroup', methods=[
    'POST',
])
@login_required
def leavegroup():
    '''退出组

    @@@
    ### 说明
    退出组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    userid = g.userid
    groupid = g.args.get('groupid', None)
    if not groupid:
        return make_err_response('组id不能为空!')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    grpRcd = dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd not in grpRcd.users:
        return make_err_response('用户不存在当前组中，无法删除!')

    try:
        grpRcd.users.remove(userRcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()