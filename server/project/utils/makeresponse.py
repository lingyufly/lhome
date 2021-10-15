#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-10-15 10:51:15
    @LastEditTime: 2021-10-15 11:42:59
'''

from flask import jsonify

def make_response(data={}, code=0, msg=''):
    return jsonify(code=code, msg=msg, data=data)