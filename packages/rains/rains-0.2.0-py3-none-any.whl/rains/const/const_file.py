# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

import pathlib

from pathlib import Path


class ConstDirNaming(object):
    """[ 常量 :: 文件夹命名 ]

    * NOT MESSAGE

    """

    LOGS: str = 'Logs'
    """ [ 常量 :: 文件夹命名 :: 日志 ] """

    DATA: str = 'Data'
    """ [ 常量 :: 文件夹命名 :: 数据 ] """


class ConstFileNaming(object):
    """[ 常量 :: 文件命名 ]

    * NOT MESSAGE

    """

    DB: str = 'RainsDatabase.db'
    """ [ 常量 :: 文件命名 :: 数据库 ] """


class ConstPath(object):
    """[ 常量 :: 路径 ]

    * NOT MESSAGE

    """

    ROOT: Path = pathlib.Path().cwd()
    """ [ 常量 :: 路径 :: 项目所在目录 ] """

    LOGS: Path = ROOT.joinpath(ConstDirNaming.LOGS)
    """ [ 常量 :: 路径 :: 项目日志目录 ] """

    DATA: Path = ROOT.joinpath(ConstDirNaming.DATA)
    """ [ 常量 :: 路径 :: 项目数据目录 ] """

    DATA_DB: Path = DATA.joinpath(ConstFileNaming.DB)
    """ [ 常量 :: 路径 :: 项目数据库文件 ] """
