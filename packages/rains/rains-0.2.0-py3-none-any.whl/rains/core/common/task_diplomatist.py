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
[ 任务外交代理 ]

"""

import time
import json

from rains.server.db import DB
from rains.server.db import SQL
from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD
from rains.core.common.action_recorder import ACTION_RECORDER


# ----------------------------------
class TaskDiplomatist(object):
    """
    [ 任务外交代理 ]

    * 该类将代理任务执行过程中的数据库写入事务以及日志输出.

    """

    _driver_id: int
    """ [ 驱动ID ] """

    _task_id: int
    """ [ 任务ID ] """

    _task_type: str
    """ [ 任务类型 ] """

    _task_created_date: str
    """ [ 任务创建日期 ] """

    _task_start_time: str
    """ [ 任务开始时间 ] """

    _task_start_timestamp: int
    """ [ 任务开始时间戳 ] """

    _case_all_count: int = 0
    """ [ 所有用例计数 ] """

    _case_pass_count: int = 0
    """ [ 通过用例计数 ] """

    _case_fail_count: int = 0
    """ [ 失败用例计数 ] """

    # ------------------------------
    def __init__(self, driver_id: int, task_type: str):
        """
        [ 任务外交代理 ]
        
        ---
        参数:
            driver_id { int } : 核心ID.
            task_type { str } : 任务类型.
        
        """

        self._driver_id = driver_id
        self._task_type = task_type

    # ------------------------------
    def created_task(self, task_name: str, task_remark: str) -> int:
        """
        [ 记录任务 ]

        ---
        参数:
            task_name { str } : 任务名称.
            task_remark { str } : 任务注释.
        
        """

        # 记录任务开始时间
        self._task_created_date = time.strftime('%Y-%m-%d')
        self._task_start_time = time.strftime('%H:%M:%S')
        self._task_start_timestamp = int(time.time())

        # 录入数据库任务记录
        self._task_id = DB.write(SQL.task.add({
            KEYWORD.ARG.NAME: task_name,
            KEYWORD.ARG.TYPE: self._task_type,
            KEYWORD.ARG.REMARK: task_remark,
            KEYWORD.ARG.CREATED_DATE: self._task_created_date,
            KEYWORD.ARG.STATE: CONST.STATE.RUN
        }))

        return self._task_id

    # ------------------------------
    def created_case(self, case_name: str, case_remark: str) -> int:
        """
        [ 记录用例 ]

        ---
        参数:
            case_name { str } : 用例名称.
            case_remark { str } : 用例注释.

        """

        case_id = DB.write(SQL.case.add({
            KEYWORD.ARG.TID: self._task_id,
            KEYWORD.ARG.NAME: case_name,
            KEYWORD.ARG.REMARK: case_remark,
            KEYWORD.ARG.CREATED_DATE: self._task_created_date
        }))

        self._case_all_count += 1

        return case_id

    # ------------------------------
    def update_case(self, cid: int, state: str, start_time: str, start_timestamp: int):
        """
        [ 更新用例 ]
        
        ---
        参数:
            cid { int } : 用例ID.
            state { str } : 用例状态.
            start_time { str } : 开始时间.
            start_timestamp { str } : 开始时间戳.

        """

        # 录入数据库更新用例
        DB.write(SQL.case.update({
            KEYWORD.ARG.CID: cid, 
            KEYWORD.ARG.STATE: state, 
            KEYWORD.ARG.START_TIME: start_time, 
            KEYWORD.ARG.END_TIME: time.strftime('%H:%M:%S'), 
            KEYWORD.ARG.SPEND_TIME_S: (int(time.time()) - start_timestamp), 
            KEYWORD.ARG.RUN_STEP: json.dumps(ACTION_RECORDER.take(self._driver_id))
        }))

        if state == CONST.STATE.END:
            self._case_pass_count += 1

        if state == CONST.STATE.ERR:
            self._case_fail_count += 1

    # ------------------------------
    def end(self, state: str):
        """
        [ 结束 ]

        ---
        参数:
            state { str } : 任务状态.
        
        """

        task_end_time = time.strftime('%H:%M:%S')

        # 更新数据库任务记录
        DB.write(SQL.task.update({
            KEYWORD.ARG.TID: self._task_id, 
            KEYWORD.ARG.STATE: state, 
            KEYWORD.ARG.START_TIME: self._task_start_time, 
            KEYWORD.ARG.END_TIME: task_end_time, 
            KEYWORD.ARG.SPEND_TIME_S: (int(time.time()) - self._task_start_timestamp), 
            KEYWORD.ARG.CASE_ALL: self._case_all_count, 
            KEYWORD.ARG.CASE_PASS: self._case_pass_count, 
            KEYWORD.ARG.CASE_FAIL: self._case_fail_count
        }))

        # 保存事务
        DB.commit()
