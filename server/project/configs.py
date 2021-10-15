#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-01-05 18:12:56
    @LastEditTime: 2021-10-15 17:33:15
'''

# 数据库地址
DB_URI = "sqlite:///sqlite.db"

# sqlalchemy 配置
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# 密钥
# SECRET_KEY = os.urandom(24)
SECRET_KEY = '1234567890'
EXPIRES_IN=3600
# session过期时间
#PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# 调试模式
DEBUG = True

# 用户头像存储地址
PHOTODIR = 'static/'

# 监听端口
PORT=5000