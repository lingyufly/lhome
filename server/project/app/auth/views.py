########################################
# auth manage
########################################
import json

from functools import wraps
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session)

from db.db import get_db

mauth=Blueprint('mauth', __name__)

# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('userid'):
            return func(*args, **kwargs)
        else:
            return jsonify({'code':-1, 'msg':'login first'})
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params=request.form
        userid=params.get('userid',None) 
        if userid is None:
            return jsonify({'code':-1,'msg':'userid is none'})
        try:
            userid=int(userid)
        except Exception as err:
            return jsonify({'code':-1,'msg':'get userid error: %s' %(str(err))})
        if userid!=session.get('userid') and session.get('isadmin')!=True:
            return jsonify({'code':-1,'msg':'Dosen\'t have authority'})
        else:
            return func(*args, **kwargs)
    return wrapper


def login_user(userid, isadmin=False):
    session['userid']=userid
    session['isadmin']=isadmin
    session.permanent=True

def logout_user(userid):
    session['userid']=userid
    session['isadmin']=False
    session.pop('userid')
    session.pop('isadmin')
    session.clear()

@mauth.route('login', methods=['POST',])
def login():
    args=request.form
    username=args.get('username',None) 
    password=args.get('password', None) 
    if username is None or password is None:
        return jsonify({'code':-1,'msg':'username or password is none'})

    db=get_db()

    try:
        res=db.execute('select userid, username, password, isadmin from user_tab where username=?', (username,)).fetchone()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: %s' %(str(err))})
    if res is not None and res[1]==username and res[2]==password:
        login_user(res[0], True if res[3]==1 else False)
        return jsonify({'code':0,'msg':'user login'})
    else:
        return jsonify({'code':-1,'msg':'username or password is wrong'})

@mauth.route('logout', methods=['POST',])
@login_required
@admin_required
def logout():
    args=request.form
    userid=args.get('userid',None) 
    if userid is None:
        return jsonify({'code':-1,'msg':'userid is none'})
    logout_user(userid)
    return jsonify({'code':0,'msg':'user logout'})


