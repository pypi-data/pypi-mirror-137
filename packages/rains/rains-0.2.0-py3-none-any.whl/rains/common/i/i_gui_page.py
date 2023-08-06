# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


from abc import ABCMeta
from abc import abstractmethod


class IGuiPage(metaclass=ABCMeta):
    """
    [ GUI页面接口 ]
    * 无

    """

    @abstractmethod
    def open(self, *args):
        """
        [ 打开页面 ]
        * 无

        [ 必要参数 ]
        * 无

        [ 可选参数 ]
        * 无

        [ 返回内容 ]
        * 无

        """

    @abstractmethod
    def _show(self, *args):
        """
        [ 渲染页面 ]
        * 无

        [ 必要参数 ]
        * 无

        [ 可选参数 ]
        * 无

        [ 返回内容 ]
        * 无

        """

    @abstractmethod
    def _event(self, *args):
        """
        [ 处理事件 ]
        * 无

        [ 必要参数 ]
        * 无

        [ 可选参数 ]
        * 无

        [ 返回内容 ]
        * 无

        """
