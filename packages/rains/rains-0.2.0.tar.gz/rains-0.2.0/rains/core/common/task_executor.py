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
[ Rains.Core.Common.TaskExecutor ]

"""

import time
from typing import Any

from rains.baseic.log import LOG
from rains.baseic.const import CONST
from rains.baseic.config import CONFIG
from rains.baseic.keyword import KEYWORD
from rains.core.common.action_recorder import ACTION_RECORDER
from rains.core.common.task_fn_agency import TaskFnAgency
from rains.core.common.task_diplomatist import TaskDiplomatist
from rains.core.common.task_instruction import TaskInstruction


# ----------------------------------
class TaskExecutor(object):
    """
    [ 任务执行器 ]

    * 任务的消费者, 它负责接收任务, 并解析运行.

    """

    _driver: Any
    """ [ 套件驱动程序 ] """

    _task_fn_agency: TaskFnAgency
    """ [ 函数代理 ] """

    _task_diplomatist: TaskDiplomatist
    """ [ 任务外交代理 ] """
    
    _task_instruction: TaskInstruction
    """ [ 任务指令 ] """

    # ------------------------------
    def __init__(self, driver: Any):
        """
        [ 任务执行器 ]

        ---
        参数:
            driver_id { int } : 核心ID.
            task_type { str } : 任务类型.
            driver { Any } : 套件驱动程序.
            plant { Any } : 套件构建工厂.

        """

        self._driver = driver
        self._task_fn_agency = TaskFnAgency(driver.plant)
        self._task_diplomatist = TaskDiplomatist(driver.driver_id, driver.project_type)

    # ------------------------------
    def running(self, task: Any):
        """
        [ 开始任务 ]

        * 接收一个 task, 并执行该 task.

        ---
        参数:
            task { Any } : 任务对象, 可以是实现 ITask 接口的任务类, 或者是 JSON 串译文.

        """
        
        self._task_instruction = TaskInstruction()

        if not isinstance(task, dict):
            self._task_instruction.convert_code_task(task)
            self._consumption_task_code()
            
        else:
            self._task_instruction.convert_json_task(task)
            self._consumption_task_json()

    # ------------------------------
    def _consumption_task_code(self):
        """
        [ 执行 CODE 任务 ]
        
        """

        task_map_living: Any
        try:
            task_map_living = self._task_instruction.task_class()
        except BaseException as error:
            raise Exception(error)
        task_map_living.plant = self._driver.plant
        task_state = CONST.STATE.END

        self._driver.running()
        
        try:
            # 创建任务记录
            driver_id = self._driver.driver_id
            task_name = self._task_instruction.task_name
            self._task_diplomatist.created_task(task_name, self._task_instruction.task_remark)
            LOG.info(f'Driver[{ driver_id }] >> 开始任务 >> [ { task_name } ]')

            # 执行任务初始化
            self._running_code_setter_instruction(KEYWORD.TASK.SET_TASK_INIT, task_map_living)

            # 执行步骤指令集
            for case_name, case_function in self._task_instruction.case_instructions.items():

                # 执行用例初始化
                self._running_code_setter_instruction(KEYWORD.TASK.SET_CASE_INIT, task_map_living)

                # 执行用例
                self._execute_code_case(case_name, task_map_living, case_function)

                # 执行任务注销
                self._running_code_setter_instruction(KEYWORD.TASK.SET_CASE_QUIT, task_map_living)

                # 引擎重置
                self._driver.reset()

            # 执行任务注销
            self._running_code_setter_instruction(KEYWORD.TASK.SET_TASK_QUIT, task_map_living)

        except BaseException as error:
            task_state = CONST.STATE.ERR
            LOG.info(f'Driver[{ driver_id }] >> 由于未知异常任务被迫中止:: { error }')
        
        finally:
            self._driver.end()
            
            # 更新数据库任务记录
            self._task_diplomatist.end(task_state)
            LOG.info(f'Driver[{ driver_id }] >> 完成任务 >> [ { task_name } ]')

    # ------------------------------
    def _running_code_setter_instruction(self, setter: str, living: Any):
        """
        [ 执行 CODE 设置器指令 ]
        
        """
        
        if self._task_instruction.setter_instructions[setter]:
            self._task_instruction.setter_instructions[setter](living)

    # ------------------------------
    def _execute_code_case(self, case_name: str, task_map_living: Any, case_function: Any):
        """
        [ 执行 CODE 任务用例 ]

        ---
        参数:
            case_name { str } : 用例名称.
            task_map_living { Any } : 任务类实例.
            case_function { Any } : 用例函数对象.

        """

        # 创建用例记录
        case_remark = 'NULL'
        if case_function.__doc__:
            case_remark = case_function.__doc__.strip()
        case_id = self._task_diplomatist.created_case(case_name, case_remark)
        
        case_state: str
        case_result: bool
        case_start_time = time.strftime("%H:%M:%S")
        case_start_timestamp = int(time.time())
        try:
            LOG.info(f'Driver[{ self._driver.driver_id }] >> 开始用例 >> [ { case_name } ]')

            # 执行用例
            result = case_function(task_map_living)

            # 如果用例返回 True 或者未返回 False 都判断为用例通过
            if result is True or result is None:
                case_state = CONST.STATE.END
                case_result = True

            # 如果用例返回 False 则判断用例失败
            else:
                case_state = CONST.STATE.ERR
                case_result = False

        # 如果用例执行过程发生异常则判断用例失败
        except BaseException as error:
            if CONFIG.debug:
                LOG.info(f'用例执行失败 : { error }')
            case_state = CONST.STATE.ERR
            case_result = False

        # 更新用例记录
        finally:
            LOG.info(f'Driver[{ self._driver.driver_id }] >> 完成用例 >> [ { case_name } ] >> [ { case_result } ]')
            ACTION_RECORDER.write(self._driver.driver_id, f'用例执行结果 >> [{ case_result }]')

            self._task_diplomatist.update_case(
                case_id, 
                case_state, 
                case_start_time, 
                case_start_timestamp
            )

    # ------------------------------
    def _consumption_task_json(self):
        """
        [ 执行译文任务 ]
        
        """
        
        task_state = CONST.STATE.END

        # 运行引擎
        self._driver.running()

        try:
            # 创建任务记录
            driver_id = self._driver.driver_id
            task_name = self._task_instruction.task_name
            self._task_diplomatist.created_task(task_name, self._task_instruction.task_remark)
            LOG.info(f'Driver[{ driver_id }] >> 开始任务 >> [ { task_name } ]')

            # 执行任务初始化
            self._running_json_setter_instruction(KEYWORD.TASK.SET_TASK_INIT)

            # 执行步骤指令集
            for case_name, case_dict in self._task_instruction.case_instructions.items():

                # 执行用例初始化
                self._running_json_setter_instruction(KEYWORD.TASK.SET_CASE_INIT)

                # 执行用例
                self._execute_json_case(case_name, case_dict)

                # 执行用例注销
                self._running_json_setter_instruction(KEYWORD.TASK.SET_CASE_QUIT)
                
                # 引擎重置
                self._driver.reset()

            # 执行任务注销
            self._running_json_setter_instruction(KEYWORD.TASK.SET_TASK_QUIT)

        except BaseException as error:
            task_state = CONST.STATE.ERR
            LOG.info(f'Driver[{ driver_id }] >> 由于未知异常任务被迫中止:: { error }')
        
        finally:
            self._driver.end()
            
            # 更新数据库任务记录
            self._task_diplomatist.end(task_state)
            LOG.info(f'Driver[{ driver_id }] >> 完成任务 >> [ { task_name } ]')

    # ------------------------------
    def _running_json_setter_instruction(self, setter: str):
        """
        [ 执行 JSON 设置器指令 ]
        
        """
        
        if self._task_instruction.setter_instructions[setter]:
            self._task_fn_agency.map(self._task_instruction.setter_instructions[setter])

    # ------------------------------
    def _execute_json_case(self, case_name: str, case_dict: dict):
        """
        [ 执行 JSON 用例 ]

        ---
        参数:
            case_name { str } : 用例名称.
            case_dict { dict } : 用例字典.

        """

        # 创建用例记录
        case_remark = 'NULL'
        if not case_dict['case_remark']:
            case_remark = case_dict['case_remark'].strip()

        case_id = self._task_diplomatist.created_case(case_name, case_remark)
        
        case_state: str
        case_result: bool
        case_start_time = time.strftime("%H:%M:%S")
        case_start_timestamp = int(time.time())

        step_return_dict: dict = {}
        try:
            # 执行用例
            for k, v in case_dict['step_list'].items():
                r = self._task_fn_agency.map(v)
                step_return_dict.update({k: r})
            
            if len(case_dict['assert']) > 0:
                for k, v in case_dict['assert'].items():
                    if step_return_dict[k] == v:
                        case_state = CONST.STATE.END
                        case_result = True
                    else:
                        case_state = CONST.STATE.ERR
                        case_result = False
            else:
                case_state = CONST.STATE.END
                case_result = True

        # 如果用例执行过程发生异常则判断用例失败
        except BaseException as err:
            LOG.debug(f'{ err }')
            case_state = CONST.STATE.ERR
            case_result = False

        # 更新用例记录
        finally:
            LOG.info(f'Driver[{ self._driver.driver_id }] >> 完成用例 >> [ { case_name } ] >> [ { case_result } ]')
            ACTION_RECORDER.write(self._driver.driver_id, f'用例执行结果 >> [{ case_result }]')

            self._task_diplomatist.update_case(
                case_id, 
                case_state, 
                case_start_time, 
                case_start_timestamp
            )
