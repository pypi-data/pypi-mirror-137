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
[ 字段关键字 ]

"""


# ----------------------------------
class KeywordArg(object):
    """ [ 字段关键字 ] """

    TID: str = 'tid'
    """ [ 任务编号 ] """

    CID: str = 'cid'
    """ [ 用例编号 ] """

    NAME: str = 'name'
    """ [ 名称 ] """

    TYPE: str = 'type'
    """ [ 类型 ] """

    REMARK: str = 'remark'
    """ [ 备注信息 ] """

    CREATED_DATE: str = 'created_date'
    """ [ 创建日期 ] """

    STATE: str = 'state'
    """ [ 状态 ] """

    START_TIME: str = 'start_time'
    """ [ 开始时间 ] """

    END_TIME: str = 'end_time'
    """ [ 结束时间 ] """

    SPEND_TIME_S: str = 'spend_time_s'
    """ [ 消耗时间(秒) ] """

    CASE_ALL: str = 'case_all'
    """ [ 所有用例计数 ] """

    CASE_PASS: str = 'case_pass'
    """ [ 成功的用例计数 ] """

    CASE_FAIL: str = 'case_fail'
    """ [ 失败的用例计数 ] """

    RUN_STEP: str = 'run_step'
    """ [ 运行步骤 ] """
