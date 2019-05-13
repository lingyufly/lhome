#########################################################################
# File Name:      main.py
# Author:         ly
# Created Time:   Fri 21 Dec 2018 10:03:55 AM CST
# Description:    
#########################################################################
# -*- coding: utf-8 -*-



from flask import Flask, flash, redirect, render_template, request, url_for
from flask_cors import *

def createapp():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app, support_credentials=True)
    import config
    app.config.from_object('config')

    from db import db
    db.init_app(app)
    from app.user.views import muser
    app.register_blueprint(muser, url_prefix='/user/')
    from app.auth.views import mauth
    app.register_blueprint(mauth, url_prefix='/auth/')
    from app.testajax.views import testajax 
    app.register_blueprint(testajax, url_prefix='/testajax/')

    return app

app=createapp()

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000)
