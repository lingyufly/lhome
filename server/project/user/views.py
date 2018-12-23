########################################
# user manage
########################################
import json

from functools import wraps
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session)

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
        res=db.execute('select count(*) from user where username= ? ', [username,]).fetchone()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: '+str(err)})

    if res[0]==0:
        return jsonify({'code':0,'msg':'username is valid'})
    else:
        return jsonify({'code':-1,'msg':'username is unvalid'})


@muser.route('register', methods=['POST',])
def register():
    args=request.form
    username=args.get('username',None) 
    password=args.get('password', None) 
    if username is None or password is None:
        return jsonify({'code':-1,'msg':'username or password is none'})
    
    description=args.get('description', None)
    birthday=args.get('birthday', None)
    gender=args.get('gender', 'Unknow')
    email=args.get('email', None)
    mobile=args.get('mobile', None)

    columns='username, password, isadmin'
    vv='?,?,?'
    vals=[username, password, False]
    if description is not None:
        columns+=',description'
        vv+=',?'
        vals.append(description)
    if birthday is not None:
        columns+=',birthday'
        vv+=',?'
        vals.append(birthday)
    if gender is not None:
        columns+=',gender'
        vv+=',?'
        vals.append(gender)
    if email is not None:
        columns+=',email'
        vv+=',?'
        vals.append(email)
    if mobile is not None:
        columns+=',mobile'
        vv+=',?'
        vals.append(mobile)

    sql='insert into user('+columns+') values('+vv+');'
    db=get_db()
    try:
        db.execute(sql, vals)
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: '+str(err)})

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
        db.execute('delete from user where id= ?;', (userid,))
        db.commit()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: '+str(err)})
    return jsonify({'code':0,'msg':'delete ok'})


@muser.route('modifyuser', methods=['POST',])
@login_required
@admin_required
def modifyuser():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})
    return jsonify({'code':0,'msg':'modify ok'})
