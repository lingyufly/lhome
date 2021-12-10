# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

from flask import jsonify

CODE_OK=0
CODE_ERR=1
CODE_SQLERR=2

def make_response(data={}, code=CODE_OK, msg=''):
    return jsonify(code=code, msg=msg, data=data)


def make_ok_response(data={}):
    return make_response(data=data)

def make_err_response(msg, code=CODE_ERR):
    return make_response(code=code, msg=msg)

def make_sqlerr_response(err):
    return make_response(code=CODE_SQLERR, msg='执行SQL失败: {}'.format(err))