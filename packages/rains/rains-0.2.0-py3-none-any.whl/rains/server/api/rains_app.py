#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright 2022. quinn.7@foxmail.com All rights reserved.
# Author :: cat7
# Email  :: quinn.7@foxmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
[ Flask.WebApi 应用程序 ]

"""

from flask import Flask
from flask.blueprints import Blueprint

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.baseic.decorator import singleton_pattern

from rains.server.api.blueprint import __all__ as blueprint_all


# ----------------------------------
@singleton_pattern
class RainsApp(object):
    """
    [ RainsApi 应用程序 ]

    * 基于 Flask 实现的 Flask.WebApi 应用程序.

    """

    _app_living: Flask = Flask(__name__)
    """ [ 应用程序实例 ] """

    # ------------------------------
    def __init__(self):
        """ 
        [ RainsApi 应用程序 ]
        
        """

        self.update_config({'JSON_AS_ASCII': False})

        for blueprint in blueprint_all:
            self.load_blueprint(blueprint)

    # ------------------------------
    @property
    def living(self) -> Flask:
        """
        [ 应用程序实例 ]

        * 返回应用程序实例.

        ---
        返回:
            Flask : Flask 应用程序实例.

        """

        return self._app_living

    # ------------------------------
    def update_config(self, config_dict: dict) -> None:
        """
        [ 更新配置项 ]

        * 更新 Flask 应用程序的配置项.

        ---
        参数:
            config { dict } : 配置字典.

        """

        self._app_living.config.update(config_dict)

        if CONFIG.debug:
            for ck, cv in config_dict.items():
                LOG.info(f'{ self.__class__.__name__ } :: 更新配置 :: [{ ck } = { cv }]')

    # ------------------------------
    def load_blueprint(self, blueprint: Blueprint):
        """
        [ 载入蓝图 ]

        * 将蓝图对象载入 Flask 应用程序.

        ---
        参数:
            blueprint { Blueprint } : Flask.Blueprint 蓝图对象.

        """

        self._app_living.register_blueprint(blueprint)

        if CONFIG.debug:
            LOG.info(f'{ self.__class__.__name__ } :: 载入蓝图 :: [{ blueprint }]')
