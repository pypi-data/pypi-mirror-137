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
[ 全局常量 ]

"""

from rains.baseic.const.const_api import ConstApi
from rains.baseic.const.const_state import ConstState
from rains.baseic.const.const_sys import ConstSys
from rains.baseic.const.const_type import ConstType


# ----------------------------------
class Const(object):
    """ [ 全局常量 ] """

    # ------------------------------
    @property
    def API(self) -> ConstApi:
        """ [ 接口常量 ] """
        return ConstApi

    # ------------------------------
    @property
    def STATE(self) -> ConstState:
        """ [ 状态常量 ] """
        return ConstState

    # ------------------------------
    @property
    def SYS(self) -> ConstSys:
        """ [ 系统常量 ] """
        return ConstSys

    # ------------------------------
    @property
    def TYPE(self) -> ConstType:
        """ [ 类型常量 ] """
        return ConstType


CONST: Const = Const()
""" [ 全局常量 ] """
