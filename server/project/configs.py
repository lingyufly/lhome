# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: 
'''

import os
from datetime import timedelta


class DevConfig(object):
    '''
    调试模式下的配置文件
    '''
    # 调试模式
    ENV="development"
    DEBUG = True

    # 日志
    LOGGER = "app"

    # SQLALCHEMY 配置
    # 数据库地址
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"
    # 动态追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示原始SQL语句
    SQLALCHEMY_ECHO = True
    # 数据库连接池大小
    # SQLALCHEMY_POOL_SIZE = 10
    # 数据库连接池超时时间
    # SQLALCHEMY_POOL_TIMEOUT = 10
    # 连接池达到最大值后可以创建的连接数
    # SQLALCHEMY_MAX_OVERFLOW = 2

    # 密钥
    SECRET_KEY = '1234567890'
    EXPIRES_IN = 3600

    # session过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 静态资源（上传、下载）存储地址
    STATIC_DIR = "static/"
    PHOTODIR = STATIC_DIR + '/photo/'

    # 监听端口
    PORT = 5000
    #SERVER_NAME="0.0.0.0:5000"


class PropConfig(DevConfig):
    '''
    部署模式配置文件
    '''
    ENV="production"
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    PORT = 8000


# Config = PropConfig
Config=DevConfig
