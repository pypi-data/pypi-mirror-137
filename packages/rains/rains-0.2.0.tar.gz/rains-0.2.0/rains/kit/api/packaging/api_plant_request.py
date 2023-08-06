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
[ Rains.Kit.Api.Packaging.ApiPlantRequest ]

"""

from typing import Any
from typing import Union

import requests
from flask import Response

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.baseic.tools import Regular
from rains.core.common.action_recorder import ACTION_RECORDER


# ----------------------------------
class ApiPlantResponse(object):
    """
    [ Api 响应对象 ]
    
    """

    _base_response: Response

    # ------------------------------
    def __init__(self, response: Response):
        """
        [ Api 响应对象 ]
        
        """

        self._base_response = response

    # ------------------------------
    @property
    def ok(self) -> Union[dict, None]:
        """
        [ 数据 ]
        
        """
        
        return self._base_response.ok

    # ------------------------------
    @property
    def data(self) -> Union[dict, None]:
        """
        [ 数据 ]
        
        """
        
        if self._base_response.ok:
            try:
                return self._base_response.json()
            except BaseException:
                return self._base_response.text


# ----------------------------------
class ApiPlantRequest(object):
    """
    [ Api请求器 ]

    """

    _api_driver: Any
    """ [ 引擎对象 ] """

    # ------------------------------
    def __init__(self, driver: Any):
        """
        [ Api请求器 ]

        ---
        参数:
            driver { WebEngine } : Web引擎对象.

        """

        self._api_driver = driver

    # ------------------------------
    @property
    def send(self):
        """
        [ Web视图'发送'相关函数 ]

        """

        return _ApiPlantHandlerMapGet(self._api_driver)

    # ------------------------------
    def _map_send(self):
        return self.send


# ----------------------------------
class _ApiPlantRequestMapBase(object):
    """
    [ Api请求器映射基础类 ]

    """

    _handler: Any
    _driver_id: int

    # ------------------------------
    def __init__(self, api_driver: Any):
        """
        [ Api请求器映射基础类 ]

        ---
        参数:
            api_driver { ApiDriver } : Web引擎对象.

        """

        self._handler = api_driver
        self._driver_id = api_driver.driver_id


# ----------------------------------
class _ApiPlantHandlerMapGet(_ApiPlantRequestMapBase):
    """
    [ Api请求器'发送'相关函数 ]

    """

    # ------------------------------
    def get(self, url: str) -> ApiPlantResponse:
        """
        [ GET ]

        ---
        参数:
            url { URL } : URL.

        """

        try:
            message = Regular.get_function_doc_name(self.get.__doc__)
            base_requests = requests.get(url, headers=self._handler.headers)
            execution_step_record(self._driver_id, message, url)
            return ApiPlantResponse(base_requests)

        except BaseException as error:
            raise ApiPlantRequestFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def post(self, url: str, data: dict) -> ApiPlantResponse:
        """
        [ POST ]

        ---
        参数:
            url { URL } : URL.
            data { dict } : 请求数据.

        """

        try:
            message = Regular.get_function_doc_name(self.get.__doc__)
            base_requests = requests.post(url, data=data, headers=self._handler.headers)
            execution_step_record(self._driver_id, message, url)
            return ApiPlantResponse(base_requests)

        except BaseException as error:
            raise ApiPlantRequestFunctionRunError(self._driver_id, message, error)


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
class ApiPlantRequestFunctionRunError(Exception):
    """ [ Api请求器函数执行异常 ] """
    
    def __init__(self, driver_id: int, message: str, error: Any):
        self.message = f'error :: { message } :: { error } !'
        self.err_name = Regular.get_function_doc_name(self.__doc__)
        execution_step_record(driver_id, message, level='error')

    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', self.message])
