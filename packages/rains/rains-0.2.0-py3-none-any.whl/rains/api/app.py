# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

from flask import Flask
from .blueprint import __all__ as blueprint_all


# 创建应用
rains_app = Flask(__name__)
""" [ RainsApi 应用 ] """

# 更新配置
rains_app.config.update({'JSON_AS_ASCII': False})

# 注册蓝图
for blueprint in blueprint_all:
    print(blueprint)
    rains_app.register_blueprint(blueprint)
