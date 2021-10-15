#!/usr/bin/env python
# coding=utf-8
'''
    @Author: Lingyu
    @Date: 2021-10-15 08:39:22
    @LastEditTime: 2021-10-15 16:38:07
'''

from jinja2.utils import F


def create_app():
    from flask import Flask
    app = Flask(__name__)

    from flask_cors import CORS
    CORS(app, support_credentials=True)

    import configs
    app.config.from_object(configs)

    from utils.hook import hook_init
    hook_init(app)
    
    from models import db
    db.init_app(app)

    from user import user
    app.register_blueprint(user, url_prefix='/user')
    from auth import mauth
    app.register_blueprint(mauth, url_prefix='/auth')

    return app



