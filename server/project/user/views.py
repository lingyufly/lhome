#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-01-05 18:12:56
    @LastEditTime: 2021-10-15 17:42:43

用户管理部分
包含用户的注册、删除、修改和查询功能。
'''

from flask import request, g

from . import user
from auth.views import login_required, userisgroupadmin
from models import dbse
from models.users import User, Group
from utils import logger, make_response
import configs

def usernameValid(username):
    rcd = dbse.query(User).filter(User.name == username).first()
    return False if rcd else True

@user.route('checkusername', methods=[
    'POST',
])
def checkusername():
    '''检查用户名是否冲突
    
    @@@
    ### 说明
    检查用户名是否冲突
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | username | string | M | 用户名 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args
    username = args.get('username', None)
    if username is None:
        return make_response(code=1, msg='用户名为空')

    if not usernameValid(username):
        return make_response(code=1, msg='用户名不可用')
    else:
        return make_response(code=0, data={})


@user.route('registeruser', methods=[
    'POST',
])
def registeruser():
    '''用户注册
    @@@
    ### 说明
    用户注册
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | username | string | M | 用户名 |
    | password | string | M | 密码 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args

    username = args.get('username', None)
    password = args.get('password', None)

    if not username or not password:
        return make_response(code=1, msg='用户名或密码为空')

    if not usernameValid(username):
        return make_response(code=1, msg='用户名不可用')

    userRcd = User()
    userRcd.name = username
    userRcd.password = password
    userRcd.gender = args.get('gender', None)
    userRcd.birthday = args.get('birthday', None)
    userRcd.email = args.get('email', None)
    userRcd.mobile = args.get('mobile', None)

    try:
        dbse.add(userRcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.format(err))
    return make_response(code=0, data={})


@user.route('deleteuser', methods=[
    'POST',
])
@login_required
def deleteuser():
    ''' 注销用户
    @@@
    ### 说明
    注销用户
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    userid = g.userid
    rcd = dbse.query(User).filter(User.id == userid).first()
    if not rcd:
        return make_response(code=1, msg='user {} not exit'.format(userid))

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.format(err))
    return make_response(code=0, data={})


@user.route('modifyuser', methods=[
    'POST',
])
@login_required
def modifyuser():
    '''修改用户信息
    @@@
    ### 说明
    修改用户信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | username | string | O | 用户名 |
    | password | string | O | 密码 |
    | gender | int | O | 性别 |
    | birthday | string | O | 生日 |
    | email | string | O | 邮箱 |
    | mobile | string | O | 手机号 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    args = g.args
    userid = g.userid
    if userid is None:
        return make_response(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_response(code=1, msg='userid dosen\'t exit')

    if args.get('username', None):
        # 更新用户名前先检查用户名是否合法
        if not usernameValid(args.get('username')):
            return make_response(code=1, msg='username is unvalid')
        userRcd.name = args.get('username', None)

    if args.get('password', None):
        userRcd.password = args.get('password')

    if args.get('gender', None):
        userRcd.gender = args.get('gender')

    if args.get('birthday', None):
        userRcd.birthday = args.get('birthday')

    if args.get('email', None):
        userRcd.email = args.get('email')

    if args.get('mobile', None):
        userRcd.mobile = args.get('mobile')

    try:
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.form(err))

    return make_response(code=0, data={})


@user.route('getuserinfo', methods=[
    'POST',
])
@login_required
def getuserinfo():
    ''' 查询用户信息
    @@@
    ### 说明
    查询用户信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | userid | string | M | 用户id |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    userid = g.args.get('userid', None)
    if userid is None:
        return make_response(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_response(code=1, msg='userid dose\'n exit')

    return make_response(code=0, data=userRcd.to_dict())


@user.route('uploadphoto', methods=[
    'POST',
])
@login_required
def uploadphoto():
    ''' 上传用户头像
    @@@
    ### 说明
    上传用户头像
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    userid = g.userid
    if userid is None:
        return make_response(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_response(code=1, msg='userid dose\'n exit')

    photo = request.files.get('photo', None)
    if photo is None:
        return make_response(code=1, msg='upload photo error')

    filename = 'photo_{:0>5d}.png'.format(int(userid))
    try:
        dir = configs.PHOTODIR
        photo.save(dir + filename)
    except Exception as err:
        return make_response(code=1, msg='save photo error: {}'.form(err))

    userRcd.photo = filename
    try:
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.form(err))

    return make_response(code=0, data={})


@user.route('queryuser', methods=[
    'POST',
])
@login_required
def queryuser():
    '''根据用户名模糊查询用户信息
    @@@
    ### 说明
    根据用户名模糊查询用户信息
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | username | string | O | 用户名 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''
    username = g.args.get('username', None)
    rcds = []
    if username:
        rcds = dbse.query(User).filter(User.name.like('%' + username +
                                                      '%')).all()
    else:
        rcds = dbse.query(User).all()

    userinfos = []
    for rcd in rcds:
        userinfos.append({'id': rcd.id, 'username': rcd.name})

    return make_response(code=0, data=userinfos)


'''
组管理部分

包含组的注册、删除、修改和查询功能。
'''


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
        return make_response(code=1, msg='groupname is none')

    if not groupnameValid(groupname):
        return make_response(code=1, msg='groupname is unvalid')
    else:
        return make_response(code=0, data={})


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
    | description | string | M | 描述 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
    '''

    userid = g.userid
    args = g.args

    groupname = args.get('groupname', None)
    description = args.get('description', None)

    if not groupname:
        return make_response(code=1, msg='groupname is none')

    groupRcd = Group()
    groupRcd.name = groupname
    groupRcd.description = description

    groupRcd.users=[dbse.query(User).filter(User.id == userid).first()]

    try:
        dbse.add(groupRcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.format(err))
    return make_response(code=0, data={})


@user.route('deletegroup', methods=[
    'POST',
])
@login_required
@userisgroupadmin
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
        return make_response(code=1, msg='group {} not exit'.format(groupid))

    rcd = dbse.query(Group).filter(Group.id == groupid).first()
    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.format(err))
    return make_response(code=0, data={})


@user.route('modifygroup', methods=[
    'POST',
])
@login_required
@userisgroupadmin
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
        return make_response(code=1, msg='groupid is none')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return make_response(code=1, msg='group dose\'nt exit')

    if args.get('groupname', None):
        groupRcd.name = args.get('groupname', None)
    if args.get('description', None):
        groupRcd.description = args.get('description', None)

    try:
        dbse.commit()
    except Exception as err:
        return make_response(code=1, msg='exec sql error: {}'.form(err))

    return make_response(code=0, data={})


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
        return make_response(code=1, msg='groupid is none')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return make_response(code=1, msg='group dose\'n exit')

    data=groupRcd.to_dict()
    data["users"]=[]
    for user in groupRcd.users:
        data['users'].append(user.to_dict())
    return make_response(code=0, data=data)


@user.route('inviteuser', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def inviteuser():
    ''' 邀请用户进组
    @@@
    ### 说明
    邀请用户进组
    
    ### 请求
    | 字段 | 字段类型 | 可选/必选 | 字段描述 |
    | groupid | integer | M | 用户组id |
    | userid | integer | M | 被邀请用户id |
    | isadmin | bool | o | 新用户是否作为管理员 |

    ### 返回
    | 字段 | 字段类型 | 字段描述 |

    @@@
        
    '''
    args = g.args
    groupid = args.get('groupid')
    userid = args.get('userid')
    isadmin = args.get('isadmin', False)

    if groupid is None or userid is None:
        return make_response(code=1, msg='group id or user id is none')

    userRcd=dbse.query(User).filter(User.id == userid).first()
    grpRcd=dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd is None or grpRcd is None:
        return make_response(code=1, msg='用户或组信息错误')

    if userRcd in grpRcd.users:
        return make_response(code=1, msg='用户已经在该组中')

    grpRcd.users.append(userRcd)

    try:
        dbse.commit()
    except Exception as e:
        return make_response(code=1, msg='保存失败：{}'.format(e))

    return make_response(code=0, data={})


@user.route('removeuser', methods=[
    'POST',
])
@login_required
@userisgroupadmin
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
        return make_response(code=1, msg='group id or user id is none')

    userRcd=dbse.query(User).filter(User.id == userid).first()
    grpRcd=dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd is None or grpRcd is None:
        return make_response(code=1, msg='用户或组信息错误')

    if userRcd not in grpRcd.users:
        return make_response(code=1, msg='用户不存在当前组中，无法删除')

    try:
        grpRcd.users.remove(userRcd)
        dbse.commit()
    except Exception as e:
        return make_response(code=1, msg='删除失败')

    return make_response(code=0, data={})


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
        return make_response(code=1, msg='groupid id is none')
    
    userRcd=dbse.query(User).filter(User.id == userid).first()
    grpRcd=dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd in grpRcd.users:
        return make_response(code=1, msg='已经加入该组，不需要重复加入')
    
    try:
        grpRcd.users.append(userRcd)
        dbse.commit()
    except Exception as e:
        return make_response(code=1, msg='保存失败：{}'.format(e))

    return make_response(code=0, data={})


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
        return make_response(code=1, msg='groupid id is none')

    userRcd=dbse.query(User).filter(User.id == userid).first()
    grpRcd=dbse.query(Group).filter(Group.id == groupid).first()

    if userRcd not in grpRcd.users:
        return make_response(code=1, msg='用户不存在当前组中，无法删除')

    try:
        grpRcd.users.remove(userRcd)
        dbse.commit()
    except Exception as e:
        return make_response(code=1, msg='保存失败：{}'.format(e))

    return make_response(code=0, data={})