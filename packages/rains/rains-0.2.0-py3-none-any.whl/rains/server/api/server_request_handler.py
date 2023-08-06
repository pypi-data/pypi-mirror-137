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
[ Rains.Api.ServerRequestHandler ]

"""

import json
from typing import Union
from werkzeug.datastructures import ImmutableMultiDict

from flask import jsonify
from flask import request
from flask import Response

from rains.baseic.const import CONST
from rains.baseic.error import ServerAnalysisParameterError
from rains.baseic.error import ServerInspectionParameterError


URL_PREFIX: str = '/api'
""" [ URL 前缀 ] """


# ----------------------------------
class ServerRequestHandler(object):
    """
    [ 服务端请求处理程序 ]
    
    * 处理 WEBAPI 请求的相关事务, 如解析前端请求参数与返回响应对象.

    """

    # ------------------------------
    @staticmethod
    def analysis_request_parameter(keys: list, must_keys: Union[list, None] = None) -> dict:
        """
        [ 解析请求参数 ]

        * 解析请求中指定 Key, 如果该值为空, 则舍弃该 Key, 而不是返回 None.

        * 如果需要确保解析结果中必须携带指定 Key, 请通过 must_keys 定义.

        ---
        示例:
            >>> params = ServerParameterHandler.analysis_request_parameter(keys=['key1', 'key2'])
            :: 该示例表示解析请求中的 key1 与 key2, 如果请求中缺失 key2, 则只返回 key1.

            >>> params = ServerParameterHandler.analysis_request_parameter(keys=['key1', 'key2'], must_keys=['key1])
            :: 该示例表示获取请求中的 key1 与 key2, 并且确保 key1 必须存在, 否则将引发异常.

        ---
        参数:
            keys { list } : 待解析的 Key 列表.
            must_keys { Union[list, None], optional } : 强制携带的 Key 列表, 默认为空.

        ---
        异常:
            ServerAnalysisParameterError : 服务端解析参数异常.
            ServerInspectionParameterError : 服务端检查参数异常.

        ---
        返回:
            dict : 返回解析完成的参数字典.

        """

        request_handle = request.args
        if request.method == 'POST':
            if not isinstance(request.form, ImmutableMultiDict):
                request_handle = request.form
            else:
                request_handle = json.loads(request.data.decode('UTF-8'))

        return ServerRequestHandler._common_analysis_request_keys(request_handle, keys, must_keys)

    # ------------------------------
    @staticmethod
    def analysis_request_headers(keys: list, must_keys: Union[list, None] = None) -> dict:
        """
        [ 解析请求头 ]

        * 解析请求头中指定 Key, 如果该值为空, 则舍弃该 Key, 而不是返回 None.
        * 如果需要确保解析结果中必须携带指定 Key, 请通过 must_keys 定义.

        ---
        示例:
            >>> params = ServerParameterHandler.analysis_request_headers(keys=['Authorization'])
            :: 该示例表示获取请求头中的 Authorization 字段, 如果请求中缺失 Authorization, 则返回空字典.

            >>> params = ServerParameterHandler.analysis_request_headers(keys=['Authorization'], must_keys=['Authorization])
            :: 该示例表示获取请求头中的 Authorization 字段, 并且确保 Authorization 必须存在, 否则将引发异常.

        ---
        参数:
            keys { list } : 待解析的 Key 列表.
            must_keys { Union[list, None], optional } : 强制携带的 Key 列表, 默认为空.

        ---
        异常:
            ServerAnalysisParameterError : 服务端解析参数异常.
            ServerInspectionParameterError : 服务端检查参数异常.

        ---
        返回:
            dict : 返回解析完成的参数字典.

        """

        headers_handle = request.headers
        return ServerRequestHandler._common_analysis_request_keys(headers_handle, keys, must_keys)

    # ------------------------------
    @staticmethod
    def successful(paras: dict) -> Response:
        """
        [ 请求成功 ]

        * 将数据序列化为 Json 并包装成 Flask.Response 响应体返回.

        ---
        参数:
            paras { dict } : 需要返回的数据.

        ---
        返回:
            Response : 响应体对象, 通过 application/json 进行操作.
         
        """

        return jsonify({
            'code'    : CONST.API.CODE_SUCCESS, 
            'message' : CONST.API.MESSAGE_SUCCESS, 
            'result'  : paras
        })

    # ------------------------------
    @staticmethod
    def unsuccessful(error: str) -> Response:
        """
        [ 请求失败 ]

        * 将数据序列化为 Json 并包装成 Flask.Response 响应体返回.

        ---
        参数:
            error { str } : 需要返回的错误内容.

        ---
        返回:
            Response : 响应体对象, 通过 application/json 进行操作.
         
        """

        return jsonify({
            'code'    : CONST.API.CODE_UNSUCCESS, 
            'message' : CONST.API.MESSAGE_UNSUCCESS, 
            'result'  : error
        })

    # ------------------------------
    @staticmethod
    def _common_analysis_request_keys(data: dict, keys: list, must_keys: list) -> dict:
        """
        [ 通用的解析参数 ]

        * analysis_request_parameter and analysis_request_headers common function.

        ---
        参数:
            data { dict } : 待解析的数据.
            keys { list } : 待解析的 Key 列表. 
            must_keys { list } : 强制携带的 Key 列表.
        
        ---
        异常:
            ServerAnalysisParameterError : 服务端解析参数异常.
            ServerInspectionParameterError : 服务端检查参数异常.

        """

        try:
            decryption_parameter: dict = {}

            # 如果 key 为空, 则丢弃, 否则储存.
            for key in keys:
                value = data.get(key)
                if not value: 
                    ...  
                else:
                    decryption_parameter.update({key: value})
            
            # 检查 keys 中是否包含所有 must_keys 的成员元素, 
            # 否则抛出 ServerAnalysisParameterError 异常.
            if must_keys:
                try:
                    for key in must_keys:
                        if not decryption_parameter[key]:
                            ...
                except KeyError as error:
                    raise ServerInspectionParameterError(error)

            return decryption_parameter

        except ServerInspectionParameterError:
            raise

        except BaseException as error:
            raise ServerAnalysisParameterError(error)
