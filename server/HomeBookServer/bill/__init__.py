from flask import Blueprint
bill = Blueprint('bill', __name__)
from .views import *
