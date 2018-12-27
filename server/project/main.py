#!/usr/bin/env python3
#########################################################################
# File Name:      main.py
# Author:         ly
# Created Time:   Fri 21 Dec 2018 10:03:55 AM CST
# Description:    
#########################################################################
# -*- coding: utf-8 -*-



from flask import Flask, flash, redirect, render_template, request, url_for
from flask_cors import *
from datetime import timedelta

def createapp():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app, support_credentials=True)
    import os
    skey=os.urandom(24)
    app.config.from_mapping(
            SECRET_KEY=skey,
            PERMANENT_SESSION_LIFETIME=timedelta(days=7),
            DATABASE='instance/db.sqlite3',
    )
    import db
    db.init_app(app)
    from user.views import muser
    app.register_blueprint(muser, url_prefix='/user/')
    from auth.views import mauth
    app.register_blueprint(mauth, url_prefix='/auth/')
    from testajax.views import testajax 
    app.register_blueprint(testajax, url_prefix='/testajax/')

    return app


if __name__ == "__main__":
    app=createapp()
    app.run("0.0.0.0", port=8000, debug=True)
