from .base import bill
from .wallet import *
from .account import *
from .accountbook import *
from .bill import *


def init_app(app, prefix="/bill"):
    app.register_blueprint(bill, url_prefix=prefix)

