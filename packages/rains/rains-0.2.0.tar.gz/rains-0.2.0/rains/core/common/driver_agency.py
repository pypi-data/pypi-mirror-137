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
[ 执行服务 ]

"""

from typing import Any

from rains.baseic.const import CONST

from rains.kit.web.web_driver import WebDriver
from rains.kit.api.api_driver import ApiDriver


# ----------------------------------
class DriverAgency(object):
    """
    [ 驱动代理 ]

    """
    
    # ------------------------------
    def start_task(self, task: Any):

        driver: Any

        if not isinstance(task, dict):

            if task.type == CONST.TYPE.PROJECT_TYPE_WEB:
                driver = WebDriver()

            if task.type == CONST.TYPE.PROJECT_TYPE_API:
                driver = ApiDriver()

        else:

            if task['task_type'] == CONST.TYPE.PROJECT_TYPE_WEB:
                driver = WebDriver()

            if task['task_type'] == CONST.TYPE.PROJECT_TYPE_API:
                driver = ApiDriver()
        
        driver.start_task(task)
