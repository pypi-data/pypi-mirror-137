# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


def singleton_pattern(cls, *args, **kwargs):
    """
    [ 单例模式装饰器 ]

    * NOT MESSAGE

    """

    instances = {}

    def _singleton_pattern():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton_pattern


CONST_SINGLETON_PATERN = singleton_pattern
"""[ 常量单例模式装饰器 ]

* NOT MESSAGE

"""

CLASS_SINGLETON_PATERN = singleton_pattern
"""[ 类单例模式装饰器 ]

* NOT MESSAGE

"""
