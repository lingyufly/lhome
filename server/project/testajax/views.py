
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify


testajax=Blueprint('testajax', __name__, template_folder='templates', static_folder='static', static_url_path='testajax')

@testajax.route('testajax/')
def testfunc():
    return render_template('testajax/index.html')