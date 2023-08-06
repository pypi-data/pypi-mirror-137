# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = [
    'RainsDbParameterHandler',
    'ConstLifecycleState',
    'ConstDbTableNaming',
    'ConstDbRunEnvironmentNaming',
    'ConstDbConfigNaming',
    'ConstDbTaskNaming',
    'ConstDbCaseNaming'
]


from rains.const.const_state import ConstLifecycleState
from rains.const.const_db import ConstDbTableNaming
from rains.const.const_db import ConstDbRunEnvironmentNaming
from rains.const.const_db import ConstDbConfigNaming
from rains.const.const_db import ConstDbTaskNaming
from rains.const.const_db import ConstDbCaseNaming


class RainsDbParameterHandler(object):
    """
    [ 数据库参数处理程序 ]

    * 该类用于解析前端请求参数，以及拼接返回给前端的 Json 数据结构。

    """

    @staticmethod
    def get_desc_limit(paras: dict) -> str:
        """
        [ 获取数据返回量区间限制 ]

        * 默认是获取 1 页， 10 条数据。

        Args:
            paras (dict): [ 参数字典 ]

        ParasMustKeys:
            page (int): [ 页数 ]
            number (int): [ 单页数据量 ]

        Returns:
            str: [ 拼接完成的 SQL LIMIT 语句参数 ]

        """

        # 获取参数
        paras = {} if not paras else paras
        page = 1 if 'page' not in paras.keys() else int(paras['page'])
        number = 10 if 'number' not in paras.keys() else int(paras['number'])

        # 计算偏移量
        limit_begin = 0
        if page > 1:
            limit_begin = (page - 1) * number

        return f'{ limit_begin }, { number }'
