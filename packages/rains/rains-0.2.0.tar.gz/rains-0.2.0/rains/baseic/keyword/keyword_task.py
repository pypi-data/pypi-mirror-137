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
[ 任务关键字 ]

"""


# ----------------------------------
class KeywordTask(object):
    """ [ 任务关键字 ] """

    SET_TASK_INIT = 'set_task_init'
    """ [ 任务初始化 ] """

    SET_TASK_QUIT = 'set_task_quit'
    """ [ 任务注销 ] """

    SET_CASE_INIT = 'set_case_init'
    """ [ 用例初始化 ] """

    SET_CASE_QUIT = 'set_case_quit'
    """ [ 用例注销 ] """

    JSON_ARG_MODULE = 'module'
    """ [ JSON字段::模块 ] """

    JSON_ARG_CLASS = 'class'
    """ [ JSON字段::类别 ] """

    JSON_ARG_FUNCTION = 'function'
    """ [ JSON字段::方法 ] """

    JSON_ARG_ELEMENT = 'element'
    """ [ JSON字段::元素 ] """

    JSON_ARG_PARAMETER = 'parameter'
    """ [ JSON字段::参数 ] """
