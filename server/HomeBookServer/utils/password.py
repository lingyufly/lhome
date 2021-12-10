# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-12-10
@Description: 密码加密和校验
'''


from werkzeug.security import generate_password_hash,check_password_hash


def hash_password(passwd):
    '''
    使用hash算法对密码加密
    '''
    return generate_password_hash(passwd)


def check_password(pwhash, passwd):
    '''
    校验密码
    '''
    return check_password_hash(pwhash, passwd)