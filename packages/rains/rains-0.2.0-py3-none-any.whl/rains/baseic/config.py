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
[ 配置 ]

"""

import yaml

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD
from rains.baseic.decorator import singleton_pattern


# ----------------------------------
@singleton_pattern
class Config(object):
    """
    [ 配置 ]

    """

    _data: dict
    """ [ 配置文件数据 ] """

    _debug: bool
    """ [ 调试模式 ] """

    _driver_max_count: int
    """ [ 驱动队列最大值 ] """

    _task_max_count: int
    """ [ 任务队列最大值 ] """

    # ------------------------------
    def __init__(self):
        """
        [ 静态配置 ]

        """
        
        # 读取配置文件    
        self.load()

    # ------------------------------
    @property
    def debug(self):
        """
        [ 调试模式 ]

        """

        return self._debug

    # ------------------------------
    @property
    def driver_max_count(self):
        """
        [ 核心队列最大值 ]

        """

        return self._driver_max_count

    # ------------------------------
    @property
    def task_max_count(self):
        """
        [ 任务队列最大值 ]

        """

        return self._task_max_count

    # ------------------------------
    def load(self):
        """
        [ 读取配置 ]

        """

        with open(CONST.SYS.PATH_CONFIG_FILE, 'r', encoding='UTF-8') as f:
            self._data = yaml.load(f, Loader=yaml.FullLoader)
            self._debug = self._data[KEYWORD.CONFIG.DEBUG]
            self._driver_max_count = self._data[KEYWORD.CONFIG.DRIVER_MAX_COUNT]
            self._task_max_count = self._data[KEYWORD.CONFIG.TASK_MAX_COUNT]

    # ------------------------------
    def dump(self):
        """
        [ 存储配置 ]

        """

        with open(CONST.SYS.PATH_CONFIG_FILE, 'w', encoding='UTF-8') as f:
            yaml.dump(self._data, f, allow_unicode=True)

    # ------------------------------
    def set_debug(self, state: bool):
        """
        [ 设置调试模式 ]
        
        ---
        参数:
            state { bool } : 调试模式.

        """

        self._debug = state
        self._data[KEYWORD.CONFIG.DEBUG] = state

    # ------------------------------
    def set_core_max_count(self, number: int):
        """
        [ 设置核心队列最大值 ]
        
        ---
        参数:
            number { int } : 数值.

        """

        self._driver_max_count = number
        self._data[KEYWORD.CONFIG.DRIVER_MAX_COUNT] = number

    # ------------------------------
    def set_task_max_count(self, number: int):
        """
        [ 设置任务队列最大值 ]
        
        ---
        参数:
            number { int } : 数值.

        """

        self._task_max_count = number
        self._data[KEYWORD.CONFIG.TASK_MAX_COUNT] = number


CONFIG: Config = Config()
""" [ 静态配置实例 ] """
