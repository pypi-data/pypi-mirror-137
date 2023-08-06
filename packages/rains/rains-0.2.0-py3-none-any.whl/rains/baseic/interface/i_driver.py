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
[ 驱动器接口 ]

"""

from typing import Any

from abc import ABCMeta
from abc import abstractmethod


# ------- I DRIVER -------
class IDriver(metaclass=ABCMeta):
    """
    [ 套件驱动程序接口 ]
    
    """

    # ------------------------------
    @abstractmethod
    def plant(self):
        """
        [ 构建工厂 ]

        """
        ...

    # ------------------------------
    @abstractmethod
    def driver_id(self):
        """
        [ 驱动ID ]

        """
        ...

    # ------------------------------
    @abstractmethod
    def get_state(self) -> bool:
        """
        [ 获取驱动程序运行状态 ]

        * 获取当前驱动程序运行状态, 启动中返回 True, 否则返回 False.

        ---
        返回:
            bool : 当前引擎状态.

        """
        ...

    # ------------------------------
    @abstractmethod
    def start_task(self, task: Any):
        """
        [ 开始任务 ]

        * 接收一个 task, 并执行该 task.

        ---
        参数:
            task { Any } : 任务对象, 可以是实现 ITask 接口的任务类, 或者是 JSON 译文.

        """
        ...

    # ------------------------------
    @abstractmethod
    def running(self):
        """
        [ 运行 ]
        
        * 运行驱动程序.

        """
        ...

    # ------------------------------
    @abstractmethod
    def end(self):
        """
        [ 结束 ]

        * 结束驱动程序.

        """
        ...

    # ------------------------------
    @abstractmethod
    def reset(self):
        """
        [ 重置 ]

        * 重置驱动程序.
        * 与结束驱动程序相比, 该接口只需要将驱动程序重置为初始状态即可.

        """
        ...
