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
[ 日志模块 ]

"""

import time
import logging

from rains.baseic.const import CONST
from rains.baseic.error import CreationLogLivingError
from rains.baseic.decorator import singleton_pattern


# 日志模块配置参数
_LOGGING_LEVEL = 'DEBUG'
""" [ 记录器日志级别 ] """

_BASE_HANDLE_LEVEL = 'INFO'
""" [ 默认流处理器的日志级别 ] """

_FILE_HANDLE_LEVELS = ['DEBUG', 'INFO', 'ERROR', 'WARNING']
""" [ 文件流处理器的日志级别 ] """

_LOG_OUTPUT_STRUCTURE = logging.Formatter('[%(asctime)s] [%(levelname)7s] %(message)s')
""" [ 日志输出格式对象 ] """


# ----------------------------------
class LogMapLevel(object):
    """ [ 日志映射等级 ] """
    
    debug: str = 'debug'
    info: str = 'info'
    warning: str = 'warning'
    error: str = 'error'
    critical: str = 'critical'


# ----------------------------------
@singleton_pattern
class Log(object):
    """
    [ 日志模块 ]

    """

    _logger: logging.Logger
    """ [ 记录器对象 ] """

    # ------------------------------
    def __init__(self):
        """
        [ 日志模块 ]
        
        ---
        异常:
            CreationLogLivingError : 创建日志实例异常.

        """

        try:
            self._logger = logging.getLogger()
            self._logger.setLevel(_LOGGING_LEVEL)
            self._logger.handlers.clear()
            self._creation_base_handle()
            self._creation_file_handle()

        except BaseException as error:
            raise CreationLogLivingError(error)

    # ------------------------------
    def map(self, level: str, message: str):
        """ 
        [ 映射日志 ]
        
        ---
        参数:
            level { str } : 日志等级.
            message { str } : 输出的日志信息.

        """

        type(self).__dict__[level](self, message)

    # ------------------------------
    def debug(self, message: str):
        """
        [ 记录 DEBUG ]

        ---
        参数:
            message { str } : 输出的日志信息.

        """

        self._logger.debug(message)

    # ------------------------------
    def info(self, message):
        """
        [ 记录 INFO ]
        
        ---
        参数:
            message { str } : 输出的日志信息.

        """

        self._logger.info(message)

    # ------------------------------
    def warning(self, message):
        """
        [ 记录 WARNING ]

        ---
        参数:
            message { str } : 输出的日志信息.

        """

        self._logger.warning(message)

    # ------------------------------
    def error(self, message):
        """
        [ 记录 ERROR ]

        ---
        参数:
            message { str } : 输出的日志信息.

        """

        self._logger.error(message)

    # ------------------------------
    def critical(self, message):
        """
        [ 记录 CRITICAL ]

        ---
        参数:
            message { str } : 输出的日志信息.

        """

        self._logger.critical(message)

    # ------------------------------
    def _creation_base_handle(self):
        """
        [ 创建默认流处理器 ]

        """

        # 创建处理器
        base_handle = logging.StreamHandler()
        # 配置日志输出格式
        base_handle.setFormatter(_LOG_OUTPUT_STRUCTURE)
        # 设置处理器日志等级
        base_handle.setLevel(_BASE_HANDLE_LEVEL)
        # 注册处理器
        self._logger.addHandler(base_handle)

    # ------------------------------
    def _creation_file_handle(self):
        """
        [ 创建文件流处理器 ]
        
        """
        
        # 创建当前项目的当天日志存放目录
        date = time.strftime('%Y-%m-%d', time.localtime())
        path = CONST.SYS.PATH_LOGS_DIR.joinpath(date)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        # 创建文件处理器
        for v in _FILE_HANDLE_LEVELS:

            # 创建处理器
            file_handle = logging.FileHandler(f'{path.joinpath(f"{ v }.log")}')
            # 配置日志输出格式
            file_handle.setFormatter(_LOG_OUTPUT_STRUCTURE)
            # 设置处理器的日志等级
            file_handle.setLevel(v)
            # 注册处理器
            self._logger.addHandler(file_handle)


LOG: Log = Log()
""" [ 日志模块实例 ] """
