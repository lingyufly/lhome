########################################
# auth manage
########################################
import json

from functools import wraps
from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for, session)

from user.models import *

from . import mauth


# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('userid'):
            return func(*args, **kwargs)
        else:
            return jsonify(code=-1, msg='login first')

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params = request.form
        userid = params.get('userid', None)
        if userid is None:
            return jsonify(code=-1, msg='userid is none')
        try:
            userid = int(userid)
        except Exception as err:
            return jsonify(code=-1, msg='get userid error: {}'.format(err))
        if userid != session.get('userid') and session.get('isadmin') != True:
            return jsonify(code=-1, msg='Dosen\'t have authority')
        else:
            return func(*args, **kwargs)

    return wrapper


def login_user(userid, isadmin=False):
    session['userid'] = userid
    session['isadmin'] = isadmin
    session.permanent = True


def logout_user(userid):
    session['userid'] = userid
    session['isadmin'] = False
    session.pop('userid')
    session.pop('isadmin')
    session.clear()


@mauth.route('login', methods=['POST', 'GET'])
def login():
    args = request.form
    username = args.get('username', None)
    password = args.get('password', None)
    if username is None or password is None:
        return jsonify(code=-1, msg='username or password is none')

    res = User.query.filter_by(name=username).first()

    if res is not None and res.name == username and res.password == password:
        #临时处理，所有登陆用户都是管理员
        login_user(res.id, True)
        return jsonify(code=0, msg='user login')
    else:
        return jsonify(code=-1, msg='username or password is wrong')


@mauth.route('logout', methods=[
    'POST',
])
@login_required
def logout():
    args = request.form
    userid = args.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')
    logout_user(userid)
    return jsonify(code=0, msg='user logout')
