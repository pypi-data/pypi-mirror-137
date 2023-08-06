# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = ['SqlRunEnvironment']


from rains.db.common import ConstDbTableNaming
from rains.db.common import ConstDbRunEnvironmentNaming
from rains.db.common import RainsDbParameterHandler


class SqlRunEnvironment(object):
    """
    [ SQL语句 :: 运行环境相关 ]

    * NOT MESSAGE

    """

    @staticmethod
    def init() -> str:
        """
        [ 初始化运行环境 ]

        * NOT MESSAGE

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        INSERT INTO { ConstDbTableNaming.RUN_ENVIRONMENT } (

             id, 
             { ConstDbRunEnvironmentNaming.POOL_RUN_STATE },
             { ConstDbRunEnvironmentNaming.CORE_SIGN_COUNT },
             { ConstDbRunEnvironmentNaming.TASK_SIGN_COUNT }
        )

        VALUES (

            NULL,
            False,
            3,
            20
        )

        """

    @staticmethod
    def get() -> str:
        """
        [ 查询运行环境 ]

        * NOT MESSAGE

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 
        
        SELECT *
        
        FROM { ConstDbTableNaming.RUN_ENVIRONMENT }

        LIMIT { RainsDbParameterHandler.get_desc_limit({}) }
        
        """
