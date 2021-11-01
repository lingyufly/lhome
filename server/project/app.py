# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

def create_app():
    from flask import Flask
    app = Flask(__name__)

    from flask_cors import CORS
    CORS(app, support_credentials=True)

    from configs import Config
    app.config.from_object(Config)

    import utils, models, user, auth
    utils.init_app(app)
    models.init_app(app)
    user.init_app(app)
    auth.init_app(app)

    return app


if __name__=='__main__':
    app=create_app()
    app.run(host='0.0.0.0')

