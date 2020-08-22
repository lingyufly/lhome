from flask import Blueprint
mauth = Blueprint('mauth', __name__)
from .views import *
