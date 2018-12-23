#!/usr/bin/env python3
#########################################################################
# File Name:      db.py
# Author:         ly
# Created Time:   Fri 21 Dec 2018 05:48:20 PM CST
# Description:    
#########################################################################
# -*- coding: utf-8 -*-

import sqlite3

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
