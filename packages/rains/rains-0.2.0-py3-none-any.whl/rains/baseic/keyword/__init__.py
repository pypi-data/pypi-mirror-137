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
[ 全局关键字 ]

"""

from rains.baseic.keyword.keyword_arg import KeywordArg
from rains.baseic.keyword.keyword_db import KeywordDB
from rains.baseic.keyword.keyword_task import KeywordTask
from rains.baseic.keyword.keyword_config import KeywordConfig


# ----------------------------------
class Keyword(object):
    """ [ 全局关键字 ] """

    # ------------------------------
    @property
    def ARG(self) -> KeywordArg:
        """ [ 字段关键字 ] """
        return KeywordArg

    # ------------------------------
    @property
    def DB(self) -> KeywordDB:
        """ [ 数据库关键字 ] """
        return KeywordDB

    # ------------------------------
    @property
    def TASK(self) -> KeywordTask:
        """ [ 任务关键字 ] """
        return KeywordTask

    # ------------------------------
    @property
    def CONFIG(self) -> KeywordConfig:
        """ [ 配置关键字 ] """
        return KeywordConfig


KEYWORD: Keyword = Keyword()
""" [ 全局关键字 ] """
