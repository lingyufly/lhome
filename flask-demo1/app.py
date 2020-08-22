from flask import Flask
from db import db
import configs

app = Flask(__name__)
app.config.from_object(configs)

db.init_app(app)

from user import user
app.register_blueprint(user, url_prefix='/user')
from auth import auth
app.register_blueprint(auth, url_prefix='/auth')
