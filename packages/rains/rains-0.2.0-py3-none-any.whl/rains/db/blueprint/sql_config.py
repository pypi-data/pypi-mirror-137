# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = ['SqlConfig']


from rains.db.common import ConstDbTableNaming
from rains.db.common import ConstDbConfigNaming
from rains.db.common import RainsDbParameterHandler


class SqlConfig(object):
    """
    [ SQL语句 :: 配置相关 ]

    * NOT MESSAGE

    """

    @staticmethod
    def add(paras: dict) -> str:
        """
        [ 新增配置 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            name (str): [ 配置名称 ]
            core_maxsize (int): [ 核心最大值 ]
            task_maxsize (int): [ 任务最大值 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        INSERT INTO { ConstDbTableNaming.CONFIG } (

             { ConstDbConfigNaming.ID },
             { ConstDbConfigNaming.NAME },
             { ConstDbConfigNaming.CORE_MAXSIZE },
             { ConstDbConfigNaming.TASK_MAXSIZE }
        )

        VALUES (

            NULL,
            '{ paras[ConstDbConfigNaming.NAME] }',
            { paras[ConstDbConfigNaming.CORE_MAXSIZE] },
            { paras[ConstDbConfigNaming.TASK_MAXSIZE] }
        )

        """

    @staticmethod
    def get(paras: dict | None = None) -> str:
        """
        [ 查询配置 ]

        * NOT MESSAGE

        Args:
            paras (dictorNone): [ 参数字典 ]
        
        ParasOptionKeys:
            page (int): [ 页数 ]
            number (int): [ 单页数据量 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 
        
        SELECT *
        
        FROM { ConstDbTableNaming.CONFIG }

        LIMIT { RainsDbParameterHandler.get_desc_limit(paras) }
        
        """
