########################################
# auth manage
########################################
import json

from functools import wraps
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session)

from db import get_db

mauth=Blueprint('mauth', __name__)

# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return jsonify({'code':-1, 'msg':'login first'})
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method =='POST':
            params=request.form
        else:
            param=request.args
        username=params.get('username',None) 
        if username is None:
            return jsonify({'code':-1,'msg':'username is none'})
        if username!=session.get('username') and session.get('isadmin')!=True:
            return jsonify({'code':-1,'msg':'Dosen\'t have authority'})
        else:
            return func(*args, **kwargs)
    return wrapper


def login_user(username, isadmin=False):
    session['username']=username
    session['isadmin']=isadmin
    session.permanent=True

def logout_user(username):
    session['username']=username
    session['isadmin']=False
    session.pop('username')
    session.pop('isadmin')
    session.clear()



@mauth.route('login', methods=['POST',])
def login():
    if request.method =='POST':
        args=request.form
    else:
        args=request.args
    username=args.get('username',None) 
    password=args.get('password', None) 
    if username is None or password is None:
        return jsonify({'code':-1,'msg':'username or password is none'})

    db=get_db()

    try:
        res=db.execute('select username, password, isadmin from user where username=?', (username,)).fetchone()
    except Exception as err:
        return jsonify({'code':-1,'msg':'exec sql error: '+str(err)})
    if res is not None and res[0]==username and res[1]==password:
        login_user(username, True if res[2]==1 else False)
        return jsonify({'code':0,'msg':'user login'})
    else:
        return jsonify({'code':-1,'msg':'username or password is wrong'})

@mauth.route('logout', methods=['POST',])
@login_required
def logout():
    if request.method =='POST':
        args=request.form
    else:
        args=request.args
    username=args.get('username',None) 
    if username is None:
        return jsonify({'code':-1,'msg':'username is none'})
    logout_user(username)
    return jsonify({'code':0,'msg':'user logout'})
