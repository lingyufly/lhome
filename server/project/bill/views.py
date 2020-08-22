########################################
# bill manager
########################################
import json

from functools import wraps
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for, session)

from db.db import get_db

from app.auth.views import login_required

mbill=Blueprint('mbill', __name__)

@mbill.route('createbillbook', methods=['POST',])
@login_required
def createbillbook():
    args=request.form
    bookname=args.get('bookname', None)
    if bookname is None:
        return jsonify(code=-1, msg='Book name is none')
    userid=args.get('id', None)
    if userid is None:
        return jsonify(code=-1, msg='userid is none')
    description=args.get('description', '')
    db=get_db()
    try:
        sql='insert into billbook_tab(bookname, id, description) values(?,?,?);'
        db.execute(sql, (bookname, userid, description))
    except Exception as err:
        return jsonify(code=-1, msg='exec sql error: %s' %(str(err)))

    res=db.execute('select bookid from billbook_tab where bookname=? and id=?;', (bookname, userid)).fetchone()
    bookid=res[0]



@mbill.route('deletebillbook', methods=['POST',])
@login_required
def deletebillbook():
    pass

@mbill.route('modifybillbook', methods=['POST',])
@login_required
def modifybillbook():
    pass

@mbill.route('addusertobillbook', methods=['POST',])
@login_required
def addusertobillbook():
    pass

@mbill.route('deleteuserfrombillbook', methods=['POST',])
@login_required
def deleteuserfrombillbook():
    pass

@mbill.route('addbill', methods=['POST',])
@login_required
def addbill():
    pass

@mbill.route('deletebill', methods=['POST',])
@login_required
def deletebill():
    pass

@mbill.route('modifybill', methods=['POST',])
@login_required
def modifybill():
    pass