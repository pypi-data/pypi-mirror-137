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
[ 创建环境 ]

"""

import yaml

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD


BASE_CONFIGURATION_DICT = {
    KEYWORD.CONFIG.DEBUG: True, 
    KEYWORD.CONFIG.DRIVER_MAX_COUNT: 3, 
    KEYWORD.CONFIG.TASK_MAX_COUNT: 50
}
""" [ 默认配置字典 ] """


# ------------------------------
def create_runtime_environment():
    """ 
    [ 创建运行环境 ] 
    
    * 创建项目运行所依赖的日志目录、数据目录、数据库文件以及配置文件.
    
    """

    # 创建项目目录
    CONST.SYS.PATH_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    CONST.SYS.PATH_DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONST.SYS.PATH_DB_FILE.touch(mode=0o777)

    # 如果不存在配置文件, 则创建默认配置文件
    if not CONST.SYS.PATH_CONFIG_FILE.exists():
        CONST.SYS.PATH_CONFIG_FILE.touch(mode=0o777)
        with open(CONST.SYS.PATH_CONFIG_FILE, 'w', encoding='UTF-8') as f:
            yaml.dump(BASE_CONFIGURATION_DICT, f, allow_unicode=True)


# ------------------------------
def create_project_template():
    """ [ 创建项目模板 ] """

    CONST.SYS.PATH_ROOT.joinpath('task').mkdir(parents=True, exist_ok=True)
    CONST.SYS.PATH_ROOT.joinpath('rains.ini').touch(mode=0o777)
