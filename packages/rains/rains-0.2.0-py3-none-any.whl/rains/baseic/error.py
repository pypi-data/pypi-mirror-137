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
[ 错误类型 ]

"""

from rains.baseic.tools import Regular


# ----------------------------------
class _RainsBaseError(Exception):
    """ [ 自定义异常基类 ] """
    def __init__(self, error: BaseException):
        self.message = str(error)
        self.err_name = Regular.get_function_doc_name(self.__doc__)
    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', self.message])


# ----------------------------------
class CreationLogLivingError(_RainsBaseError):
    """ [ 创建日志实例异常 ] """


# ----------------------------------
class ServerAnalysisParameterError(_RainsBaseError):
    """ [ 服务端解析参数异常 ] """


# ----------------------------------
class ServerInspectionParameterError(_RainsBaseError):
    """ [ 服务端检查参数异常 ] """
    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', f'参数 [{ self.message }] 是必须的 !'])


# ----------------------------------
class WebFindHandleFindElementError(_RainsBaseError):
    """ [ Web定位器获取元素异常 ] """


# ----------------------------------
class RainsDbInitError(_RainsBaseError):
    """ [ Rains 数据库初始化异常 ] """


# ----------------------------------
class RainsDbReadError(_RainsBaseError):
    """ [ Rains 数据库读取异常 ] """


# ----------------------------------
class RainsDbWriteError(_RainsBaseError):
    """ [ Rains 数据库写入异常 ] """


# ----------------------------------
class TaskInstructionError(Exception):
    """ [ 任务指令解析异常 ] """
