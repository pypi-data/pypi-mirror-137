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
[ Rains.Kit.Api.ApiDriver ]

"""

import random

from rains.baseic.const import CONST
from rains.baseic.interface.i_driver import IDriver
from rains.core.common.task_executor import TaskExecutor

from rains.kit.api.api_plant import ApiPlant


API_DRIVER_SIGN_ID_LIST = []
""" [ 驱动程序编号池 ] """


# ----------------------------------
class ApiDriver(IDriver):
    """
    [ Api 驱动程序 ]

    """

    _driver_id: int
    """ [ 驱动程序ID ] """

    _state: bool = False
    """ [ 运行状态 ] """
    
    _plant: ApiPlant = None
    """ [ 构建工厂对象 ] """

    _task_executor: TaskExecutor
    """ [ 任务执行器 ] """

    _project_type: str = CONST.TYPE.PROJECT_TYPE_API
    """ [ 项目类型 ] """

    _headers: dict = {
        'Authorization': 'NULL',
        'User-Agent'   : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    }
    """ [ 头部信息 ] """

    # ------------------------------
    def __init__(self):
        """
        [ Web 驱动程序 ]

        """

        # 生成随机ID并创建驱动程序
        while True:
            self._driver_id = random.randint(100, 999)

            if self._driver_id not in API_DRIVER_SIGN_ID_LIST:
                API_DRIVER_SIGN_ID_LIST.append(self._driver_id)
                break
            else:
                continue
            
        self._plant = ApiPlant(self)
        self._task_executor = TaskExecutor(self)

    # ------------------------------
    @property
    def plant(self):
        """
        [ 构建工厂 ]

        """

        return self._plant

    # ------------------------------
    @property
    def driver_id(self):
        """
        [ 驱动ID ]

        """

        return self._driver_id

    # ------------------------------
    @property
    def project_type(self):
        """
        [ 项目类型 ]

        """

        return self._project_type

    # ------------------------------
    @property
    def headers(self):
        """
        [ 头部信息 ]

        """

        return self._headers

    # ------------------------------
    def set_headers(self, new_headers: dict):
        """
        [ 设置头部信息 ]

        ---
        参数:
            new_headers { dict } : 新的请求头字典.

        """
        
        self._headers = new_headers

    # ------------------------------
    def get_state(self) -> bool:
        """
        [ 获取引擎运行状态 ]

        * 获取引擎运行状态, 启动中返回 True, 否则返回 False. 

        Returns:
            bool: [ 引擎运行状态 ]

        """

        return self._state

    # ------------------------------
    def start_task(self, task):
        """
        [ 开始任务 ]

        * 接收一个 task, 并执行该 task.

        ---
        参数:
            task { Any } : 任务对象, 可以是实现 ITask 接口的任务类, 或者是 JSON 串译文.

        """

        self._task_executor.running(task)

    # ------------------------------
    def running(self):
        """
        [ 运行引擎 ]

        * 驱动与定位器的实例化.

        """

        if not self._state:
            self._state = True

    # ------------------------------
    def end(self):
        """
        [ 结束引擎 ]

        * 退出并销毁当前持有的驱动与定位器. 

        """

        if self._state:
            self._state = False

    # ------------------------------
    def reset(self):
        """
        [ 重置引擎 ]

        * 将引擎重置至初始阶段.
        * 与 end() 相比, 该函数只是重置引擎至初始状态, 而不是注销.

        """

        if self._state:
            ...
