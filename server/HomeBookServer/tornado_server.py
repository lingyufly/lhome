# -*- coding: utf-8 -*-
'''
@Author: Lingyu
@Date: 2021-10-19
@Description: windows系统中部署脚本
'''

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import create_app
from configs import Config

if __name__ == '__main__':
    app=create_app()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(Config.PORT)
    IOLoop.instance().start()