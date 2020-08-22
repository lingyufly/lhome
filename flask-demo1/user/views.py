from app import app
from flask import Response, request, json, make_response

from .models import *

from . import user


@user.route('/list')
def user_list():
    users = User.query.all()
    val = {'count': len(users), 'vals': []}
    for u in users:
        v = {'id': u.id, 'name': u.username}
        val['vals'].append(v)

    return json.dumps(val)


@user.route('/add')
def user_add():
    for i in range(0, 10000):
        name = str(i)
        user = User(username=name)
        db.session.add(user)
    db.session.commit()
    return "ok"
