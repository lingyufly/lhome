#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-13 16:06:17
@LastEditTime: 2021-10-15 09:39:03
'''

from functools import wraps


# login_required 装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, c=1)

    return wrapper


def login_required11(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('c' in kwargs.keys())
        print(*args)
        print(args)
        print(kwargs['c'])
        return func(*args, **kwargs)

    return wrapper


@login_required
@login_required11
def aa(c):
    print(c)


aa()
