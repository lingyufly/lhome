from app import app
from flask import Response, request, json, make_response

from .models import *

from . import auth


@auth.route('/list')
def user_list():
    users = User.query.all()
    val = {'users': users}
    return json.dumps(val)


@auth.route('/add')
def user_add():
    id = request.values['id']
    name = request.values['name']
    user = User(id=id, username=name)
    db.session.add(user)
    db.session.commit()
    return "ok"
