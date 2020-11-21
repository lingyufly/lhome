########################################
# user manage
########################################
import json
from functools import wraps
import random
from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for, session, current_app)

from auth.views import login_required, userisgroupadmin

from db import db, dbse
from . import user
from .models import User, Group, UserGroupRelationship
'''
用户管理部分

包含用户的注册、删除、修改和查询功能。
'''


def usernameValid(username):
    rcd = dbse.query(User).filter(User.name == username).first()
    return False if rcd else True


@user.route('usernamecheck', methods=[
    'POST',
])
def usernamecheck():
    '''
    检查用户名是否冲突
    '''
    args = request.form
    username = args.get('username', None)
    if username is None:
        return jsonify(code=1, msg='username is none')

    if not usernameValid(username):
        return jsonify(code=1, msg='username is unvalid')
    else:
        return jsonify(code=0, data={})


@user.route('registeruser', methods=[
    'POST',
])
def registeruser():
    '''
    用户注册
    '''
    args = request.form

    username = args.get('username', None)
    password = args.get('password', None)

    if not username or not password:
        return jsonify(code=1, msg='username or password is none')

    if not usernameValid(username):
        return jsonify(code=1, msg='username is unvalid')

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
        return jsonify(code=1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, data={})


@user.route('deleteuser', methods=[
    'POST',
])
@login_required
def deleteuser(tokenData):
    '''
    删除用户。
    '''
    userid = tokenData.get('userid')
    rcd = dbse.query(User).filter(User.id == userid).first()
    if not rcd:
        return jsonify(code=1, msg='user {} not exit'.format(userid))

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as err:
        return jsonify(code=1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, data={})


@user.route('modifyuser', methods=[
    'POST',
])
@login_required
def modifyuser(tokenData):
    '''
    修改用户信息
    '''
    args = request.form
    userid = tokenData.get('userid')
    if userid is None:
        return jsonify(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=1, msg='userid dose\'n exit')

    if args.get('username', None):
        # 更新用户名前先检查用户名是否合法
        if not usernameValid(username):
            return jsonify(code=1, msg='username is unvalid')
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
        return jsonify(code=1, msg='exec sql error: {}'.form(err))

    return jsonify(code=0, data={})


@user.route('getuserinfo', methods=[
    'POST',
])
@login_required
def getuserinfo(tokenData):
    '''
    查询用户信息
    '''
    userid = request.form.get('userid', None)
    if userid is None:
        return jsonify(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=1, msg='userid dose\'n exit')

    return jsonify(code=0, data=userRcd.to_dict())


@user.route('uploadphoto', methods=[
    'POST',
])
@login_required
def uploadphoto(tokenData):
    '''
    上传用户头像
    '''
    args = request.form
    userid = tokenData.get('userid')
    if userid is None:
        return jsonify(code=1, msg='userid is none')

    userRcd = dbse.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=1, msg='userid dose\'n exit')

    photo = request.files.get('photo', None)
    if photo is None:
        return jsonify(code=1, msg='upload photo error')

    filename = 'photo_{:0>5d}.png'.format(int(userid))
    try:
        dir = current_app.config['PHOTODIR']
        photo.save(dir + filename)
    except Exception as err:
        return jsonify(code=1, msg='save photo error: {}'.form(err))

    userRcd.photo = filename
    try:
        dbse.commit()
    except Exception as err:
        return jsonify(code=1, msg='exec sql error: {}'.form(err))

    return jsonify(code=0, data={})


@user.route('queryuser', methods=[
    'POST',
])
@login_required
def queryuser(tokenData):
    '''
    根据用户名模糊查询用户信息
    '''
    username = request.form.get('username', None)
    rcds = []
    if username:
        rcds = dbse.query(User).filter(User.name.like('%' + username +
                                                      '%')).all()
    else:
        rcds = dbse.query(User).all()

    userinfos = []
    for rcd in rcds:
        userinfos.append({'id': rcd.id, 'username': rcd.name})

    return jsonify(code=0, data=userinfos)


'''
组管理部分

包含组的注册、删除、修改和查询功能。
'''


def groupnameValid(groupname):
    rcd = dbse.query(Group).filter(Group.name == groupname).first()
    return False if rcd else True


@user.route('groupnamecheck', methods=[
    'POST',
])
def groupnamecheck():
    '''
    检查组名是否冲突
    '''
    args = request.form
    groupname = args.get('groupname', None)
    if groupname is None:
        return jsonify(code=1, msg='groupname is none')

    if not groupnameValid(groupname):
        return jsonify(code=1, msg='groupname is unvalid')
    else:
        return jsonify(code=0, data={})


@user.route('registergroup', methods=[
    'POST',
])
@login_required
def registergroup(tokenData):
    '''
    注册组
    '''

    userid = tokenData.get('userid')
    args = request.form

    groupname = args.get('groupname', None)
    description = args.get('description', None)

    if not groupname:
        return jsonify(code=1, msg='groupname is none')

    groupRcd = Group()
    groupRcd.name = groupname
    groupRcd.description = description

    try:
        dbse.add(groupRcd)
        dbse.flush()

        # 自动将当前用户作为组管理员
        relRcd = UserGroupRelationship()
        relRcd.userid = userid
        relRcd.groupid = groupRcd.id
        relRcd.userisadmin = True
        dbse.add(relRcd)
        dbse.commit()
    except Exception as err:
        return jsonify(code=1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, data={})


@user.route('deletegroup', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def deletegroup(tokenData):
    '''
    删除组

    删除组和用户对应关系
    '''
    groupid = request.form.get('groupid')
    rcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not rcd:
        return jsonify(code=1, msg='group {} not exit'.format(groupid))

    relrcds = dbse.query(UserGroupRelationship).filter(
        UserGroupRelationship.groupid == groupid).all()
    try:
        dbse.delete(rcd)

        # 删除关联表
        for rcd in relrcds:
            dbse.delete(rcd)

        dbse.commit()
    except Exception as err:
        return jsonify(code=1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, data={})


@user.route('modifygroup', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def modifygroup(tokenData):
    '''
    修改组信息
    '''
    args = request.form
    groupid = args.get('groupid')
    if groupid is None:
        return jsonify(code=1, msg='groupid is none')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return jsonify(code=1, msg='group dose\'nt exit')

    if args.get('groupname', None):
        groupRcd.name = args.get('groupname', None)
    if args.get('description', None):
        groupRcd.description = args.get('description', None)

    try:
        dbse.commit()
    except Exception as err:
        return jsonify(code=1, msg='exec sql error: {}'.form(err))

    return jsonify(code=0, data={})


@user.route('setgroupadmin', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def setgroupadmin(tokenData):
    '''
    更新组员的管理权限

    如果更新后一个管理员也没有，则将当前用户当作管理员

    参数：
        必选：
            groupid：要维护的组id
            users[]：组员id和管理员标记列表
                userid：组员id
                isadmin：管理员标记
        可选：
    返回：
    '''
    args = request.form
    groupid = args.get('groupid')
    userList = args.get('users')

    if not userList:
        return jsonify(code=0, data={})

    try:
        # 挨个用户更新标记
        for user in userList:
            userid = user.get('userid')
            isadmin = user.get('isadmin')
            dbse.query(UserGroupRelationship).filter(
                UserGroupRelationship.groupid == groupid).filter(
                    UserGroupRelationship.userid ==
                    userid).first().userisadmin = isadmin

        dbse.flush()

        # 如果一个管理员也没有，则将当前用户继续作为管理员
        if not dbse.query(UserGroupRelationship).filter(
                UserGroupRelationship.groupid == groupid).filter(
                    UserGroupRelationship.userisadmin == True).first():
            dbse.query(UserGroupRelationship).filter(
                UserGroupRelationship.groupid == groupid).filter(
                    UserGroupRelationship.userid == tokenData.get(
                        'userid')).first().userisadmin = True

        dbse.commit()
        return jsonify(code=0, data={})
    except Exception as e:
        return jsonify(code=1, msg="更新失败: {}".format(e))


@user.route('getgroupinfo', methods=[
    'POST',
])
@login_required
def getgroupinfo(tokenData):
    '''
    根据组id查询组信息

    输入：
        必选：
            groupid：要查询的组id

        可选：
    
    返回：

    '''
    groupid = request.form.get('groupid', None)
    if groupid is None:
        return jsonify(code=1, msg='groupid is none')

    groupRcd = dbse.query(Group).filter(Group.id == groupid).first()
    if not groupRcd:
        return jsonify(code=1, msg='group dose\'n exit')

    return jsonify(code=0, data=groupRcd.to_dict())


@user.route('inviteuser', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def inviteuser(tokenData):
    '''
    邀请用户进组
    参数：
        必选：
            groupid：组id
            userid：用户id
        可选：
            isadmin：是否作为管理员
    返回：
        
    '''
    args = request.form
    groupid = args.get('groupid')
    userid = args.get('userid')
    isadmin = args.get('isadmin', False)

    if groupid is None or userid is None:
        return jsonify(code=1, msg='group id or user id is none')

    if dbse.query(UserGroupRelationship).filter(
            UserGroupRelationship.groupid == groupid).filter(
                UserGroupRelationship.userid == userid).first():
        return jsonify(code=1, msg='用户已经存在该组中')

    rcd = UserGroupRelationship()
    rcd.userid = userid
    rcd.groupid = groupid
    rcd.userisadmin = isadmin

    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as e:
        return jsonify(code=1, msg='保存失败：{}'.format(e))

    return jsonify(code=0, data={})


@user.route('removeuser', methods=[
    'POST',
])
@login_required
@userisgroupadmin
def removeuser(tokenData):
    '''
    从组中删除用户

    参数：
        必选：
            groupid：组id
            userid：用户id
    '''
    args = request.form
    groupid = args.get('groupid')
    userid = args.get('userid')

    if groupid is None or userid is None:
        return jsonify(code=1, msg='group id or user id is none')

    rcd = dbse.query(UserGroupRelationship).filter(
        UserGroupRelationship.groupid == groupid).filter(
            UserGroupRelationship.userid == userid).first()

    if not rcd:
        return jsonify(code=1, msg='用户不存在当前组中，无法删除')
    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as e:
        return jsonify(code=1, msg='删除失败')

    return jsonify(code=0, data={})


@user.route('joingroup', methods=[
    'POST',
])
@login_required
def joingroup(tokenData):
    '''
    加入组

    参数：
        必选：
            groupid：待加入的组id
    
    '''
    userid = tokenData.get('userid')
    groupid = request.form.get('groupid', None)
    if not groupid:
        return jsonify(code=1, msg='groupid id is none')

    if dbse.query(UserGroupRelationship).filter(
            UserGroupRelationship.groupid == groupid).filter(
                UserGroupRelationship.userid == userid).first():
        return jsonify(code=1, msg='已经加入该组，不需要重复加入')

    rcd = UserGroupRelationship()
    rcd.userid = userid
    rcd.groupid = groupid
    rcd.userisadmin = False

    try:
        dbse.add(rcd)
        dbse.commit()
    except Exception as e:
        return jsonify(code=1, msg='保存失败：{}'.format(e))

    return jsonify(code=0, data={})


@user.route('leavegroup', methods=[
    'POST',
])
@login_required
def leavegroup(tokenData):
    '''
    退出组

    参数：
        必选：
            groupid：待退出的组id
    '''
    userid = tokenData.get('userid')
    groupid = request.form.get('groupid', None)
    if not groupid:
        return jsonify(code=1, msg='groupid id is none')

    rcd = dbse.query(UserGroupRelationship).filter(
        UserGroupRelationship.groupid == groupid).filter(
            UserGroupRelationship.userid == userid).first()

    if not rcd:
        return jsonify(code=1, msg='并未加入当前组，无法退出')

    # 如果是最后一个管理员，则无法删除
    # TODO

    try:
        dbse.delete(rcd)
        dbse.commit()
    except Exception as e:
        return jsonify(code=1, msg='保存失败：{}'.format(e))

    return jsonify(code=0, data={})