from flask import Flask
from db import db
import configs
from flask_cors import *

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_object(configs)

db.init_app(app)

from user import user
app.register_blueprint(user, url_prefix='/user')
from auth import mauth
app.register_blueprint(mauth, url_prefix='/auth')

from testajax import testajax
app.register_blueprint(testajax, url_prefix="/testajax")
