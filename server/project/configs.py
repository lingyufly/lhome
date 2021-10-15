#!/usr/bin/env python
# coding=utf-8
'''
    @Author: Lingyu
    @Date: 2021-01-05 18:12:56
    @LastEditTime: 2021-10-15 15:18:08
'''


HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask1'
USERNAME = 'root'
PASSWORD = '123456'

DB_URI = "sqlite:///sqlite.db"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#PERMANENT_SESSION_LIFETIME = timedelta(days=7)
DEBUG = True
PHOTODIR = 'static/'
