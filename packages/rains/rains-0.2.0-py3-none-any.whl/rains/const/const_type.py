# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


class ConstProjectType(object):
    """
    [ 常量 :: 项目类型 ]

    * NOT MESSAGE

    """

    WEB: str = 'CONST_PROJECT_TYPE_FROM_WEB'
    """ [ 常量 :: 项目类型 :: WEB ] """

    MINI: str = 'CONST_PROJECT_TYPE_FROM_MINI'
    """ [ 常量 :: 项目类型 :: 微信小程序 ] """


class ConstTaskType(object):
    """
    [ 常量 :: 任务类型 ]

    * NOT MESSAGE

    """

    CODE: str = 'CONST_TASK_TYPE_FROM_CODE'
    """ [ 常量 :: 任务类型 :: 代码 ] """

    JSON: str = 'CONST_TASK_TYPE_FROM_JSON'
    """ [ 常量 :: 任务类型 :: JSON 译文 ] """
