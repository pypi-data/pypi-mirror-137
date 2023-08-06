# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = [
    'RAINS_DB',
    'RAINS_SQL',
    'URL_PREFIX',
    'Response',
    'Blueprint',
    'ServerParameterHandler',
]

import json

from flask import jsonify
from flask import request
from flask import Response
from flask import Blueprint

from rains.db.rains_db import RainsDb
from rains.db.rains_sql import RainsSql
from rains.const.const_api import ConstApiStateMsg
from rains.const.const_api import ConstApiStateCode


RAINS_DB: RainsDb = RainsDb()
""" [ 数据库实例 ] """

RAINS_SQL: RainsSql = RainsSql()
""" [ SQL语句实例 ] """

URL_PREFIX: str = '/api'
""" [ URL 统一前缀 ] """


class ServerParameterHandler(object):
    """
    [ 服务端参数处理程序 ]

    * 该类用于解析前端请求参数，以及拼接返回给前端的 Json 数据结构。

    """

    def __init__(self):
        """
        [ 服务端参数处理程序 ]

        * NOT MESSAGE

        """

        ...

    @staticmethod
    def analysis_request_parameter(keys: list, must_keys: list = []) -> dict:
        """
        [ 解析请求参数 ]

        * 从请求中解析指定参数。
        * 如果解析得到的参数值为空，则舍弃该参数。
        * 如果 must_keys 不为空列表，则检查解析结果是否包含 must_keys。

        Args:
            keys (list): [ 需解析的参数 Key 列表 ]
            must_keys (list): [ 必须包含的 Key 列表 ]

        Raises:
            ServerAnalysisParameterError: [ 服务端解析参数异常 ]

        Returns:
            dict: [ 返回解析完成的参数字典 ]

        """

        try:
            request_handle = request.args
            if request.method == 'POST':
                request_handle = json.loads(request.data.decode('UTF-8'))

            decryption_paras: dict = {}
            for key in keys:
                value = request_handle.get(key)
                if not value: 
                    ...  
                else:
                    decryption_paras.update({key: value})
            
            if len(must_keys) > 0:
                ServerParameterHandler.inspection_parameter(decryption_paras, must_keys)

        except BaseException as err:
            raise ServerAnalysisParameterError(str(err))

        else:
            return decryption_paras
    
    @staticmethod
    def inspection_parameter(paras: dict, keys: list):
        """
        [ 检查参数是否包含必要 Keys ]

        * 如果 keys 的所有元素都存在于 paras 中，则通过，否则抛出 ServerAnalysisParameterError 异常。

        Args:
            paras (dict): [ 参数字典 ]
            keys (list): [ Key 列表 ]

        Raises:
            ParametersAreMissingException: [description]

        """

        for key in keys:
            try:
                if not paras[key]:
                    ...

            except KeyError as err:
                raise ServerAnalysisParameterError(str(err))

    @staticmethod
    def successful(paras: dict) -> jsonify:
        """
        [ 请求成功 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 需要返回的数据字典 ]

        Returns:
            jsonify: [ 返回前端的 Json 数据结构 ]

        """

        return jsonify({
            'code': ConstApiStateCode.SUCCESSFUL,
            'message': ConstApiStateMsg.SUCCESSFUL,
            'result': paras
        })

    @staticmethod
    def unsuccessful(err: str) -> jsonify:
        """
        [ 请求失败 ]

        * NOT MESSAGE

        Args:
            err (str): [ 需要返回的错误信息 ]

        Returns:
            jsonify: [ 返回前端的 Json 数据结构 ]

        """

        return jsonify({
            'code': ConstApiStateCode.UNSUCCESSFUL,
            'message': ConstApiStateMsg.UNSUCCESSFUL,
            'err': err
        })


class ServerAnalysisParameterError(Exception):

    def __init__(self, message: str):
        """
        [ 服务端解析参数异常 ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的错误信息 ]

        """

        self.message = message
    
    def __str__(self) -> str:
        
        return f"服务端解析参数异常:: { self.message }"
