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
[ 行为记录器 ]

"""

from rains.baseic.decorator import singleton_pattern


# ----------------------------------
@singleton_pattern
class ActionRecorder(object):
    """
    [ 行为记录器 ]

    * 用以记录一些希望后续被取出的行为信息, 通常用于多个类之间的数据交互.
    * 通过编号进行数据的写入与取出, 且取出后, 将会清空被取出编号的数据.

    """

    # 缓冲存储器
    _buffer: dict

    # ------------------------------
    def __init__(self):
        """
        [ 行为记录器 ]
 
        """

        self._buffer = {}

    # ------------------------------
    def write(self, id: int, record: str):
        """
        [ 录入信息 ]

        * 将编号的行为信息录入到缓冲存储器中.

        ---
        参数:
            id { int } : 编号.
            record { str } : 行为信息.

        """

        if id in self._buffer:
            self._buffer[id].append(record)

        else:
            self._buffer.update({id: [record]})

    # ------------------------------
    def take(self, id: int) -> list:
        """
        [ 取出信息 ]

        * 取出编号的行为信息, 清空缓冲存储器该编号的所有数据.

        ---
        参数:
            id { int } : 编号.

        ---
        返回:
            list : 核心的行为信息列表.

        """

        try:
            records = self._buffer[id]
            del self._buffer[id]
            return records
        
        except KeyError:
            return []


ACTION_RECORDER: ActionRecorder = ActionRecorder()
""" [ 行为记录器实例 ] """
