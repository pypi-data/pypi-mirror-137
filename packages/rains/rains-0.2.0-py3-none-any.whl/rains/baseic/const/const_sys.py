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
[ 系统常量 ]

"""

import pathlib
from pathlib import Path


# ----------------------------------
class ConstSys(object):
    """ [ 系统常量 ] """

    PATH_ROOT: Path = pathlib.Path().cwd()
    """ [ 运行路径 ] """

    NAME_LOGS_DIR: str = 'log'
    """ [ 日志文件夹名称 ] """

    PATH_LOGS_DIR: Path = PATH_ROOT.joinpath(NAME_LOGS_DIR)
    """ [ 日志文件夹路径 ] """

    NAME_DATA_DIR: str = 'data'
    """ [ 数据文件夹名称 ] """

    PATH_DATA_DIR: Path = PATH_ROOT.joinpath(NAME_DATA_DIR)
    """ [ 数据文件夹路径 ] """

    NAME_DB_FILE: str = 'RainsDatabase.db'
    """ [ 数据库文件名称 ] """

    PATH_DB_FILE: Path = PATH_DATA_DIR.joinpath(NAME_DB_FILE)
    """ [ 项目数据库文件 ] """

    NAME_CONFIG_FILE: str = 'RainsConfig.yaml'
    """ [ 配置文件名称 ] """

    PATH_CONFIG_FILE: Path = PATH_DATA_DIR.joinpath(NAME_CONFIG_FILE)
    """ [ 配置文件路径 ] """
