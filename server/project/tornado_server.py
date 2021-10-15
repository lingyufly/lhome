#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author: Lingyu
    @Date: 2021-10-15 17:14:57
    @LastEditTime: 2021-10-15 17:30:41
'''

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import create_app
import configs

if __name__ == '__main__':
    app=create_app()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(configs.PORT)
    IOLoop.instance().start()