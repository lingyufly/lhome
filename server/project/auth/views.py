########################################
# auth manage
########################################
import json

from functools import wraps
from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for, session, current_app)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user.models import *

from . import mauth

from db import db, dbse


def create_token(userinfo):
    '''
    生成token
    :param userinfo:用户信息
    :return: token
    '''

    #第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    #接收用户id转换与编码
    token = s.dumps(userinfo).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''

    if not token:
        return None
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    data = None
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return None
    return data


# login_required 装饰器
def login_required(func):
    '''
    装饰器，解析token数据，判断当前请求是否合法
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.form['token']
            tokenData = verify_token(token)
            if not tokenData:
                return jsonify(code=1, msg='login first')
            return func(*args, **kwargs, tokenData=tokenData)
        except Exception as e:
            return jsonify(code=1, msg='login first: {}'.format(e))

    return wrapper


def userisgroupadmin(func):
    '''
    装饰器，判断当前登陆用户是否是组的管理员，

    该装饰器必须在login_required之后使用
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('tokenData'):
            return jsonify(code=1, msg='login first')

        tokenData = kwargs.get('tokenData')

        userid = tokenData.get('userid')
        groupid = request.form.get('groupid')
        if not groupid:
            return jsonify(code=1, msg='group id is none')

        rcd = dbse.query(UserGroupRelationship).filter(
            UserGroupRelationship.groupid == groupid).filter(
                UserGroupRelationship.userid == userid).first()
        if not rcd or not rcd.userisadmin:
            return jsonify(code=1, msg='权限不足')

        return func(*args, **kwargs)

    return wrapper


@mauth.route('login', methods=['POST', 'GET'])
def login():
    '''
    登陆请求
    参数：
        必选：
            username：登陆用户名
            password：登陆密码
    '''
    args = request.form
    username = args.get('username', None)
    password = args.get('password', None)
    if username is None or password is None:
        return jsonify(code=1, msg='username or password is none')

    res = User.query.filter_by(name=username).first()

    if res is not None and res.name == username and res.password == password:
        token = create_token({'userid': res.id, 'username': res.name})
        return jsonify(code=0, data={'token': token})
    else:
        return jsonify(code=1, msg='username or password is wrong')


@mauth.route('logout', methods=[
    'POST',
])
@login_required
def logout():
    '''
    退出登录请求
    参数：
        必选：
            userid：当前登录用户的id
    '''
    args = request.form
    userid = args.get('userid', None)
    if userid is None:
        return jsonify(code=1, msg='userid is none')
    return jsonify(code=0, data={})
