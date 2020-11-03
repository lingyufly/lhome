########################################
# user manage
########################################
import json
from functools import wraps
import random
from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for, session, current_app)

from auth.views import login_required, admin_required, login_user, logout_user

from db import db
from . import user
from .models import User, Family


def usernameValid(username):
    rcd = db.session.query(User).filter(User.name == username).first()
    return False if rcd else True


@user.route('checkusername', methods=[
    'POST',
])
def checkusername():
    args = request.form
    username = args.get('username', None)
    if username is None:
        return jsonify(code=-1, msg='username is none')

    if usernameValid(username):
        return jsonify(code=-1, msg='username is unvalid')
    else:
        return jsonify(code=0, msg='username is valid')


@user.route('register', methods=[
    'POST',
])
def register():
    args = request.form

    username = args.get('username', None)
    password = args.get('password', None)

    if not username or not password:
        return jsonify(code=-1, msg='username or password is none')

    if not usernameValid(username):
        return jsonify(code=-1, msg='username is unvalid')

    userRcd = User()
    userRcd.name = username
    userRcd.password = password
    userRcd.gender = args.get('gender', None)
    userRcd.birthday = args.get('birthday', None)
    userRcd.email = args.get('email', None)
    userRcd.mobile = args.get('mobile', None)

    try:
        db.session.add(userRcd)
        db.session.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, msg='insert ok')


@user.route('deleteuser', methods=[
    'POST',
])
@login_required
@admin_required
def deleteuser():
    args = request.form
    userid = args.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    rcd = db.session.query(User).filter(User.id == userid).first()
    if not rcd:
        return jsonify(code=-1, msg='user {} not exit'.format(userid))

    try:
        rcd.delete()
        db.session.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: {}'.format(err))
    return jsonify(code=0, msg='delete ok')


@user.route('modifyuser', methods=[
    'POST',
])
@login_required
@admin_required
def modifyuser():
    args = request.form
    userid = args.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    userRcd = db.session.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=-1, msg='userid dose\'n exit')

    if args.get('username', None):
        # 更新用户名前先检查用户名是否合法
        if usernameValid(username):
            return jsonify(code=-1, msg='username is unvalid')
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
        db.session.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: {}'.form(err))

    return jsonify(code=0, msg='modify ok')


@user.route('getuserinfo', methods=[
    'POST',
])
@login_required
def getuserinfo():
    userid = request.form.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    userRcd = db.session.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=-1, msg='userid dose\'n exit')

    return jsonify(code=0, msg='get userinfo ok', result=userRcd.to_dict())


@user.route('uploadphoto', methods=[
    'POST',
])
@login_required
def uploadphoto():
    args = request.form
    userid = args.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    userRcd = db.session.query(User).filter(User.id == userid).first()
    if not userRcd:
        return jsonify(code=-1, msg='userid dose\'n exit')

    photo = request.files.get('photo', None)
    if photo is None:
        return jsonify(code=0, msg='upload photo error')

    filename = 'photo_{:0>5d}.png'.format(int(userid))
    try:
        dir = current_app.config['PHOTODIR']
        photo.save(dir + filename)
    except Exception as err:
        return jsonify(code=0, msg='save photo error: {}'.form(err))

    userRcd.photo = filename
    try:
        db.session.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: {}'.form(err))

    return jsonify(code=0, msg='upload photo ok')
