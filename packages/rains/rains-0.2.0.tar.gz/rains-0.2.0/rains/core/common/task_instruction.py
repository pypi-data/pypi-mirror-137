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
[ Rains.Common.Task.TaskInstruction ]

"""

from typing import Any

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD
from rains.baseic.error import TaskInstructionError


CASE_SPECIFICATION_NAMING = 'CASE'
""" [ 合法用例命名 ] """


# ----------------------------------
class TaskInstruction(object):
    """
    [ 任务指令 ]

    * Rains 允许通过多种方式编写自动化测试用例.
    * 为了使这些方式具备一定的兼容性, 该类将进行中间指令集的转换.

    """

    _task_name: str
    """ [ 任务名称 ] """

    _task_remark: str
    """ [ 任务注释 ] """

    _task_type: str
    """ [ 任务类型 ] """

    _task_class = None
    """ [ 任务类的类名 ] """

    _case_instructions: dict
    """ [ 用例指令集 ] """

    _setter_instructions: dict
    """ [ 设置器指令集 ] """
    
    _is_packaging: bool = False
    """ [ 是否已转换 ] """

    # ------------------------------
    def __init__(self):
        """
        [ 任务指令 ]

        """

        self._case_instructions = {}

        self._setter_instructions = {
            KEYWORD.TASK.SET_TASK_INIT: None, 
            KEYWORD.TASK.SET_TASK_QUIT: None, 
            KEYWORD.TASK.SET_CASE_INIT: None, 
            KEYWORD.TASK.SET_CASE_QUIT: None
        }

    # ------------------------------
    @property
    def task_name(self) -> str:
        """
        [ 任务类型 ]

        """

        return self._task_name

    # ------------------------------
    @property
    def task_remark(self) -> str:
        """
        [ 任务注释 ]

        """

        return self._task_remark

    # ------------------------------
    @property
    def task_type(self) -> str:
        """
        [ 任务类型 ]

        """

        return self._task_type

    # ------------------------------
    @property
    def task_class(self) -> str:
        """
        [ 任务类的类名 ]

        """

        return self._task_class

    # ------------------------------
    @property
    def case_instructions(self) -> dict:
        """
        [ 用例指令集 ]

        """

        return self._case_instructions

    # ------------------------------
    @property
    def setter_instructions(self) -> dict:
        """
        [ 设置器指令集 ]

        """

        return self._setter_instructions

    # ------------------------------
    def convert_code_task(self, task_class: Any):
        """
        [ 转换代码类型任务 ]
        
        ---
        参数:
            task_class { Any } : 继承 IKitTask 套件任务接口的任务类.

        """

        try:
            if not self._is_packaging:

                # 确认 指令集类型
                self._task_type = CONST.TYPE.TASK_TYPE_CODE
                # 获取 任务类的类名
                self._task_class = task_class
                # 读取 任务类的信息
                self._task_name = task_class.__name__
                if task_class.__doc__:
                    self._task_remark = task_class.__doc__.strip()
                else:
                    self._task_remark = 'NULL'

                # 解析指令集
                for k, v in task_class.__dict__.items():

                    # 捕获设置器指令集
                    if k in self._setter_instructions.keys() and callable(v):
                        self._setter_instructions[k] = v

                    # 捕获步骤指令集
                    if str(k[:4:]).upper() == CASE_SPECIFICATION_NAMING and callable(v):
                        self._case_instructions[k] = v

                # 完成封装
                self._is_packaging = True

            return self

        except BaseException as error:
            raise TaskInstructionError(error)


    # ------------------------------
    def convert_json_task(self, task_json: dict):
        """
        [ 转换译文类型任务 ]

        ---
        参数:
            task_json { dict } : 符合规范的 JSON 译文字典.

        """

        try:
            if not self._is_packaging:

                # 确认 指令集类型
                self._task_type = CONST.TYPE.TASK_TYPE_JSON
                # 读取 任务类的信息
                self._task_name = task_json['task_name']
                self._task_remark = task_json['task_remark']

                # 解析设置器指令集
                instructions_setter: dict = task_json['instructions_setter']
                for k, v in instructions_setter.items():
                    if k in self._setter_instructions.keys():
                        self._setter_instructions[k] = v

                # 解析用例指令集
                instructions_case: dict = task_json['instructions_case']
                for k, v in instructions_case.items():
                    if str(k[:4:]).upper() == CASE_SPECIFICATION_NAMING:
                        self._case_instructions[k] = v

                # 完成封装
                self._is_packaging = True

            return self

        except BaseException as error:
            raise TaskInstructionError(error)
