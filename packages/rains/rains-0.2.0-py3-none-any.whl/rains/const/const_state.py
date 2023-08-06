# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


class ConstSwitchState(object):
    """
    [ 常量 :: 开关状态 ]

    * NOT MESSAGE

    """

    ON: str = 'CONST_SWITCH_STATE_ON'
    """ [ 常量 :: 开关状态 :: 开 ] """

    OFF: str = 'CONST_SWITCH_STATE_OFF'
    """ [ 常量 :: 开关状态 :: 关 ] """


class ConstLifecycleState(object):
    """
    [ 常量 :: 生命周期状态 ]

    * NOT MESSAGE

    """

    RUN: str = 'CONST_LIFECYCLE_STATE_RUN'
    """ [ 常量 :: 生命周期状态 :: 运行 ] """

    END: str = 'CONST_LIFECYCLE_STATE_END'
    """ [ 常量 :: 生命周期状态 :: 停止 ] """

    ERR: str = 'CONST_LIFECYCLE_STATE_ERR'
    """ [ 常量 :: 生命周期状态 :: 异常 ] """
