#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-10-15 11:18:34
    @LastEditTime: 2021-10-15 17:36:39
'''

import configs
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_token(userinfo):
    '''
    生成token
    :param userinfo:用户信息
    :return: token
    '''

    #第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    #第二个参数是有效期(秒)
    s = Serializer(configs.SECRET_KEY, configs.EXPIRES_IN)
    #接收用户id转换与编码
    token = s.dumps(userinfo).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''

    if not token:
        return None
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(configs.SECRET_KEY)
    data = None
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return None
    return data