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
[ Rains.Kit.Api.Packaging.ApiPlantHandler ]

"""

from typing import Any

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.baseic.tools import Regular
from rains.core.common.action_recorder import ACTION_RECORDER


# ----------------------------------
class ApiPlantHandler(object):
    """
    [ Api处理器 ]

    """

    _api_driver: Any
    """ [ 引擎对象 ] """

    # ------------------------------
    def __init__(self, driver: Any):
        """
        [ Api处理器 ]

        ---
        参数:
            driver { WebEngine } : Web引擎对象.

        """

        self._api_driver = driver

    # ------------------------------
    @property
    def get(self):
        """
        [ Web视图'获取'相关函数 ]

        """

        return _ApiPlantHandlerMapGet(self._api_driver)

    # ------------------------------
    def _map_get(self):
        return self.get

    # ------------------------------
    @property
    def set(self):
        """
        [ Web视图'设置'相关函数 ]

        """

        return _ApiPlantHandlerMapSet(self._api_driver)

    # ------------------------------
    def _map_set(self):
        return self.set


# ----------------------------------
class _ApiPlantHandlerMapBase(object):
    """
    [ Api处理器映射基础类 ]

    """

    _handler: Any
    _driver_id: int

    # ------------------------------
    def __init__(self, api_driver: Any):
        """
        [ Api处理器映射基础类 ]

        ---
        参数:
            api_driver { ApiDriver } : Web引擎对象.

        """

        self._handler = api_driver
        self._driver_id = api_driver.driver_id


# ----------------------------------
class _ApiPlantHandlerMapGet(_ApiPlantHandlerMapBase):
    """
    [ Api处理器'获取'相关函数 ]

    """

    # ------------------------------
    def headers(self) -> dict:
        """
        [ 获取当前请求头字典 ]

        ---
        返回:
            dict : 当前请求头字典.

        """

        try:
            message = Regular.get_function_doc_name(self.headers.__doc__)
            headers = self._handler.headers
            execution_step_record(self._driver_id, message, headers)

            return headers

        except BaseException as error:
            raise ApiPlantHandlerFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def token(self) -> str:
        """
        [ 获取当前请求 TOKEN ]

        ---
        返回:
            str : 当前请求 TOKEN.

        """

        try:
            message = Regular.get_function_doc_name(self.token.__doc__)
            token = self._handler.headers['Authorization']
            execution_step_record(self._driver_id, message, token)

            return token

        except BaseException as error:
            raise ApiPlantHandlerFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _ApiPlantHandlerMapSet(_ApiPlantHandlerMapBase):
    """
    [ Api处理器'设置'相关函数 ]

    """

    # ------------------------------
    def add_headers(self, item: dict):
        """
        [ 新增请求头信息 ]

        ---
        参数:
            item { dict } : 新增请求头信息字典.

        """

        try:
            message = Regular.get_function_doc_name(self.add_headers.__doc__)
            headers = self._handler.headers
            headers.update(item)
            self._handler.set_headers(headers)
            execution_step_record(self._driver_id, message, item)

        except BaseException as error:
            raise ApiPlantHandlerFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def del_headers(self, key: str):
        """
        [ 删除请求头信息 ]

        ---
        参数:
            key { str } : 删除请求头信息Key.

        """

        try:
            message = Regular.get_function_doc_name(self.del_headers.__doc__)
            headers = self._handler.headers
            if key in headers.keys():
                del headers[key]
            self._handler.set_headers(headers)
            execution_step_record(self._driver_id, message, key)

        except BaseException as error:
            raise ApiPlantHandlerFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def set_token(self, token: str):
        """
        [ 设置请求 TOKEN ]

        ---
        参数:
            token { str } : 请求 TOKEN.

        """

        try:
            message = Regular.get_function_doc_name(self.set_token.__doc__)
            headers = self._handler.headers
            headers['Authorization'] = token
            self._handler.set_headers(headers)
            execution_step_record(self._driver_id, message, token)

        except BaseException as error:
            raise ApiPlantHandlerFunctionRunError(self._driver_id, message, error)


# ----------------------------------
def execution_step_record(driver_id: int, message: str, join_message: str = None, level: str = 'info'):
    """
    [ 执行步骤记录 ]

    * 执行时, 将同步将信息传递给日志服务与用例记录器.

    ---
    参数:
        driver_id { int } : 核心ID.
        message { str } : 记录信息.
        join_message { str } : 拼接信息.

    """

    if join_message:
        message = ''.join([message, ' >> ', f'[{ str(join_message) }]'])

    ACTION_RECORDER.write(driver_id, message)

    if CONFIG.debug:
        LOG.map(level, f'Driver[{ driver_id }] >> { message }')
        

# ----------------------------------
class ApiPlantHandlerFunctionRunError(Exception):
    """ [ Api处理器函数执行异常 ] """
    
    def __init__(self, driver_id: int, message: str, error: Any):
        self.message = f'error :: { message } :: { error } !'
        self.err_name = Regular.get_function_doc_name(self.__doc__)
        execution_step_record(driver_id, message, level='error')

    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', self.message])
