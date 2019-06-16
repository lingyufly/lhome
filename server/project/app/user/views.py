########################################
# user manage
########################################
import json
from functools import wraps
import random
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session, current_app)

from db.db import get_db

from app.auth.views import login_required, admin_required, login_user, logout_user

muser=Blueprint('muser', __name__)

@muser.route('checkusername', methods=['POST',])
def checkusername():
    args=request.form
    username=args.get('username', None)
    if username is None:
        return jsonify(code=-1, msg='username is none')
    db=get_db()
    try:
        res=db.execute('select count(*) from user_tab where name= ? ', [username,]).fetchone()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))

    if res[0]==0:
        return jsonify(code=0, msg='username is valid')
    else:
        return jsonify(code=-1, msg='username is unvalid')


@muser.route('register', methods=['POST',])
def register():
    args=request.form
    if args.get('username', None) is None or args.get('password', None) is None:
        return jsonify(code=-1, msg='username or password is none')

    columns=[]
    params=[]
    vals=[]
    
    username=args.get('username', None)
    password=args.get('password', None)
    createdate=args.get('createdate', None)
    description=args.get('description', None)
    gender=args.get('gender', None)
    birthday=args.get('birthday', None)
    email=args.get('email', None)
    mobile=args.get('mobile', None)

    if username is not None:
        columns.append('name')
        vals.append(username)
        params.append('?')
    if password is not None:
        columns.append('password')
        vals.append(password)
        params.append('?')
    if createdate is not None:
        columns.append('createdate')
        vals.append(createdate)
        params.append('?')
    if description is not None:
        columns.append('description')
        vals.append(description)
        params.append('?')
    if gender is not None:
        columns.append('gender')
        vals.append(gender)
        params.append('?')
    if birthday is not None:
        columns.append('birthday')
        vals.append(birthday)
        params.append('?')
    if email is not None:
        columns.append('email')
        vals.append(email)
        params.append('?')
    if mobile is not None:
        columns.append('mobile')
        vals.append(mobile)
        params.append('?')
    
    sql='insert into user_tab(%s) values(%s);' %(','.join(columns), ','.join(params))
    db=get_db()
    try:
        db.execute(sql, vals)
        db.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))
    return jsonify(code=0, msg='insert ok')


@muser.route('deleteuser', methods=['POST',])
@login_required
@admin_required
def deleteuser():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify(code=-1, msg='userid is none')
    
    db=get_db()
    try:
        db.execute('delete from user_tab where id= ?;', (userid,))
        db.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))
    return jsonify(code=0, msg='delete ok')


@muser.route('modifyuser', methods=['POST',])
@login_required
@admin_required
def modifyuser():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    columns=[]
    vals=[]
    username=args.get('username', None)
    password=args.get('password', None)
    createdate=args.get('createdate', None)
    description=args.get('description', None)
    gender=args.get('gender', None)
    birthday=args.get('birthday', None)
    email=args.get('email', None)
    mobile=args.get('mobile', None)

    if username is not None:
        columns.append('name')
        vals.append(username)
        params.append('?')
    if password is not None:
        columns.append('password')
        vals.append(password)
        params.append('?')
    if createdate is not None:
        columns.append('createdate')
        vals.append(createdate)
        params.append('?')
    if description is not None:
        columns.append('description')
        vals.append(description)
        params.append('?')
    if gender is not None:
        columns.append('gender')
        vals.append(gender)
        params.append('?')
    if birthday is not None:
        columns.append('birthday')
        vals.append(birthday)
        params.append('?')
    if email is not None:
        columns.append('email')
        vals.append(email)
        params.append('?')
    if mobile is not None:
        columns.append('mobile')
        vals.append(mobile)
        params.append('?')
    
    vals.append(userid)
    sql='update user_tab set %s where id=?;' %(','.join(columns))
    db=get_db()
    try:
        db.execute(sql, vals)
        db.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))

    return jsonify(code=0, msg='modify ok')

@muser.route('getuserinfo', methods=['POST',])
@login_required
def getuserinfo():
    userid=request.form.get('userid', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    sql='select * from user_tab where id=?;'
    db=get_db()
    try:
        res=db.execute(sql, userid).fetchone()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))
    data={key: res[i] for i, key in enumerate(res.keys())}
    return jsonify(code=0, msg='get userinfo ok', result=data)

@muser.route('uploadphoto', methods=['POST',])
@login_required
def uploadphoto():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify(code=-1, msg='userid is none')

    photo=request.files.get('photo', None)
    if photo is None:
        return jsonify(code=0, msg='upload photo error')

    filename='photo_%05d.png' % (session.get('userid'))
    try:
        dir=current_app.config['PHOTODIR']
        photo.save(dir+filename)
    except Exception as err:
        return jsonify(code=0, msg='save photo error: %s' %(str(err)))

    sql='update user_tab set photo=? where id=?;'
    db=get_db()
    try:
        db.execute(sql, [filename, userid])
        db.commit()
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))

    return jsonify(code=0, msg='upload photo ok')
