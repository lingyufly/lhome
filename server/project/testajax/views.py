
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify


testajax=Blueprint('testajax', __name__, template_folder='templates', static_folder='static', static_url_path='testajax')

@testajax.route('/')
def testfunc():
    return render_template('testajax/index.html')

@testajax.route("/testm/", methods=['GET', 'POST'])
def test():
    print(request.path)
    print(request.script_root)
    print(request.url)
    print(request.base_url)
    print(request.url_root)
    print(request.blueprint)
    return "ok"