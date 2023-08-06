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
[ 任务接口 ]

"""

from abc import ABCMeta
from abc import abstractmethod


# ------- I TASK -------
class ITask(metaclass=ABCMeta):
    """
    [ 测试套件任务接口 ]

    """

    # ------------------------------
    @abstractmethod
    def set_task_init(self):
        """
        [ 设置任务初始化 ]

        * 该接口将在 [ 任务 ] 开始时执行, 全程只会执行一次.

        """
        ...

    # ------------------------------
    @abstractmethod
    def set_task_quit(self):
        """
        [ 设置任务注销 ]

        * 该接口将在 [ 任务 ] 结束后执行, 全程只会执行一次.

        """
        ...

    # ------------------------------
    @abstractmethod
    def set_case_init(self):
        """
        [ 设置用例初始化 ]

        * 该接口将在每次 [ 用例 ] 开始时执行.

        """
        ...

    # ------------------------------
    @abstractmethod
    def set_case_quit(self):
        """
        [ 设置用例注销 ]

        * 该接口将在每次 [ 用例 ] 结束后执行.

        """
        ...
