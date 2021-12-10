# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 用户的注册、删除、修改和查询功能。
'''

from flask import request, g

from .base import user
from auth.wrapper import login_required, admin_required
from models import dbse, User, Group
from utils.makeresponse import make_ok_response, make_err_response, make_sqlerr_response
from utils.password import hash_password, check_password
from configs import Config


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
        return make_err_response('用户名不能为空!')

    if not usernameValid(username):
        return make_err_response('用户名不可用!')

    return make_ok_response()


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
        return make_err_response('用户名和密码不能为空')

    if not usernameValid(username):
        return make_err_response('用户名不可用')

    userRcd = User()
    userRcd.name = username
    userRcd.password = hash_password(password)
    userRcd.gender = args.get('gender', None)
    userRcd.birthday = args.get('birthday', None)
    userRcd.email = args.get('email', None)
    userRcd.mobile = args.get('mobile', None)

    try:
        dbse.add(userRcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


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
        return make_err_response('用户不存在')

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)
    return make_ok_response()


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
        return make_err_response('用户id不能为空')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_err_response('用户不存在')

    if args.get('username',
                None) and userRcd.name != args.get('username', None):
        # 更新用户名前先检查用户名是否合法
        if not usernameValid(args.get('username')):
            return make_err_response('用户名不可用')
        userRcd.name = args.get('username', None)

    if args.get('password', None):
        userRcd.password = hash_password(args.get('password'))

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
        return make_sqlerr_response(err)

    return make_ok_response()


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
        return make_err_response('用户id不能为空')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_err_response('用户不存在')

    data = userRcd.to_dict()
    data["groups"] = []
    for grp in userRcd.groups:
        data['groups'].append(grp.to_dict())
    return make_ok_response(data)


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
        return make_err_response('用户id不能为空')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return make_err_response('用户不存在')

    photo = request.files.get('photo', None)
    if photo is None:
        return make_err_response('上传照片失败')

    filename = 'photo_{:0>5d}.png'.format(int(userid))
    try:
        dir = Config.PHOTODIR
        photo.save(dir + filename)
    except Exception as err:
        return make_err_response('保存照片失败: {}'.form(err))

    userRcd.photo = filename
    try:
        dbse.commit()
    except Exception as err:
        return make_sqlerr_response(err)

    return make_ok_response()


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

    return make_ok_response(userinfos)
