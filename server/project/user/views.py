########################################
# user manage
########################################
import json
from functools import wraps
import random
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session, current_app)

from db import get_db

from auth.views import login_required, admin_required, login_user, logout_user

muser=Blueprint('muser', __name__)

@muser.route('checkusername', methods=['POST',])
def checkusername():
    args=request.form
    username=args.get('username', None)
    if username is None:
        return jsonify({'code':-1,'msg':'username is none'})
    db=get_db();
    try:
        res=db.execute('select count(*) from user_tab where username= ? ', [username,]).fetchone()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})

    if res[0]==0:
        return jsonify({'code':0,'msg':'username is valid'})
    else:
        return jsonify({'code':-1,'msg':'username is unvalid'})


@muser.route('register', methods=['POST',])
def register():
    args=request.form
    if args.get('username', None) is None or args.get('password', None) is None:
        return jsonify({'code':-1,'msg':'username or password is none'})

    columns=[]
    params=[]
    vals=[]
    for key, value in args.items():
        columns.append(key)
        vals.append(value)
        params.append('?')
    
    sql='insert into user_tab(%s) values(%s);' %(','.join(columns), ','.join(params))
    db=get_db()
    try:
        db.execute(sql, vals)
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})
    return jsonify({'code':0,'msg':'insert ok'})


@muser.route('deleteuser', methods=['POST',])
@login_required
@admin_required
def deleteuser():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})
    
    db=get_db()
    try:
        db.execute('delete from user_tab where userid= ?;', (userid,))
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})
    return jsonify({'code':0,'msg':'delete ok'})


@muser.route('modifyuser', methods=['POST',])
@login_required
@admin_required
def modifyuser():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})

    columns=[]
    vals=[]
    for key, value in args.items():
        if key=='userid':
            continue
        columns.append(key+'=?')
        vals.append(value)
    
    vals.append(userid)
    sql='update user_tab set %s where userid=?;' %(','.join(columns))
    db=get_db()
    try:
        db.execute(sql, vals)
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})

    return jsonify({'code':0,'msg':'modify ok'})

@muser.route('getuserinfo', methods=['POST',])
@login_required
def getuserinfo():
    userid=request.form.get('userid', None)
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})

    sql='select * from user_tab where userid=?;'
    db=get_db()
    try:
        res=db.execute(sql, userid).fetchone()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})
    data={key: res[i] for i, key in enumerate(res.keys())}
    data=json.dumps(data)
    return jsonify({'code':0,'msg':'get userinfo ok', 'data':data})

@muser.route('uploadphoto', methods=['POST',])
@login_required
def uploadphoto():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})

    photo=request.files.get('photo', None)
    if photo is None:
        return jsonify({'code':0,'msg':'upload photo error'})

    filename='photo_%05d.png' % (session.get('userid'))
    try:
        dir=current_app.config['PHOTODIR']
        photo.save(dir+filename)
    except Exception as err:
        return jsonify({'code':0,'msg':'save photo error: %s' %(str(err))})

    sql='update user_tab set photo=? where userid=?;'
    db=get_db()
    try:
        db.execute(sql, [filename, userid])
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})

    return jsonify({'code':0,'msg':'upload photo ok'})
