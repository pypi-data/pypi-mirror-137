# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


class ConstApiStateCode(object):
    """
    [ 常量 :: API 状态码 ]

    * NOT MESSAGE

    """

    SUCCESSFUL: int = 200
    """ [ 常量 :: API 状态码 :: 成功 ] """

    UNSUCCESSFUL: int = 500
    """ [ 常量 :: API 状态码 :: 失败 ] """


class ConstApiStateMsg(object):
    """
    [ 常量 :: API 状态信息 ]

    * NOT MESSAGE

    """

    SUCCESSFUL: str = '成功'
    """ [ 常量 :: API 状态信息 :: 成功 ] """

    UNSUCCESSFUL: str = '失败'
    """ [ 常量 :: API 状态信息 :: 失败 ] """
