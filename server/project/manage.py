#!/usr/bin/env python
# coding=utf-8
'''
    @Author: Lingyu
    @Date: 2021-10-15 08:39:22
    @LastEditTime: 2021-10-15 10:42:41
'''


from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db

app=create_app()

manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command("db", MigrateCommand)  # 创建数据库映射命令
manager.add_command("start", Server(port=8000, use_debugger=True))  # 创建启动命令

if __name__ == "__main__":
    manager.run()
