# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

from rains.db.blueprint.sql_task import SqlTask
from rains.db.blueprint.sql_case import SqlCase
from rains.db.blueprint.sql_config import SqlConfig
from rains.db.blueprint.sql_run_environment import SqlRunEnvironment


class RainsSql(object):
    """
    [ SQL语句映射类 ]

    * NOT MESSAGE

    """

    @property
    def run_environment(self) -> SqlRunEnvironment:
        """
        [ 运行环境相关 ]

        * NOT MESSAGE

        Returns:
            SqlRunEnvironment: [ SQL语句 :: 运行环境相关 ]

        """

        return SqlRunEnvironment

    @property
    def config(self) -> SqlConfig:
        """
        [ 配置相关 ]

        * NOT MESSAGE

        Returns:
            SqlRunEnvironment: [ SQL语句 :: 配置相关 ]

        """

        return SqlConfig

    @property
    def task(self) -> SqlTask:
        """
        [ 任务相关 ]

        * NOT MESSAGE

        Returns:
            SqlTask: [ SQL语句 :: 任务相关 ]

        """

        return SqlTask

    @property
    def case(self) -> SqlCase:
        """
        [ 用例相关 ]

        * NOT MESSAGE

        Returns:
            SqlCase: [ SQL语句 :: 用例相关 ]

        """

        return SqlCase
