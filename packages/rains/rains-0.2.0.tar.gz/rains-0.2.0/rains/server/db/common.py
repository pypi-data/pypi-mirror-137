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
[ Rains.DB.Common ]

"""


# ----------------------------------
class RainsDbParameterHandler(object):
    """
    [ 数据库参数处理程序 ]

    * 该类用于解析前端请求参数, 以及拼接返回给前端的 Json 数据结构.

    """

    # ------------------------------
    @staticmethod
    def get_desc_limit(page: int = 1, number: int = 10) -> str:
        """
        [ 获取数据返回量区间限制 ]

        * 默认是获取 1 页, 10 条数据.
        
        ---
        参数:
            page { int } : 页数.
            number { int } : 单页数据量.

        ---
        返回:
            Response : 拼接完成的 SQL LIMIT 语句参数.

        """
        
        # 计算偏移量
        limit_begin = 0
        if page > 1:
            limit_begin = (page - 1) * number

        return f'{ limit_begin }, { number }'
