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
[ Rains.DB.RainsSql ]

"""

from rains.server.db.blueprint.sql_task import SqlTask
from rains.server.db.blueprint.sql_case import SqlCase


# ----------------------------------
class RainsSql(object):
    """
    [ SQL语句映射类 ]

    """

    @property
    def task(self) -> SqlTask:
        """
        [ 任务相关 ]

        ---
        返回:
            SqlTask : SQL语句任务相关封装类.

        """

        return SqlTask

    # ------------------------------
    @property
    def case(self) -> SqlCase:
        """
        [ 用例相关 ]

        ---
        返回:
            SqlCase : SQL语句用例相关封装类.

        """

        return SqlCase
