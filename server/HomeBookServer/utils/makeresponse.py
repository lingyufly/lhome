# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from flask import jsonify

def make_response(data={}, code=0, msg=''):
    return jsonify(code=code, msg=msg, data=data)