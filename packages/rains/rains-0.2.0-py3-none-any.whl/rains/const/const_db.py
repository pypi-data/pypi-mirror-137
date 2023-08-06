# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


class ConstDbTableNaming(object):
    """
    [ 常量 :: 数据库表命名 ]

    * NOT MESSAGE

    """

    RUN_ENVIRONMENT: str = 'run_environment'
    """ [ 常量 :: 数据库表命名 :: 运行环境表 ] """

    CONFIG: str = 'configs'
    """ [ 常量 :: 数据库表命名 :: 配置表 ] """

    TASKS: str = 'tasks'
    """ [ 常量 :: 数据库表命名 :: 任务表 ] """

    CASES: str = 'cases'
    """ [ 常量 :: 数据库表命名 :: 用例表 ] """


class ConstDbRunEnvironmentNaming(object):
    """
    [ 常量 :: 运行环境表字段命名 ]

    * NOT MESSAGE

    """

    POOL_RUN_STATE: str = 'pool_run_state'
    """ [ 常量 :: 运行环境表字段命名 :: 进程池运行状态 ] """

    CORE_SIGN_COUNT: str = 'core_sign_count'
    """ [ 常量 :: 运行环境表字段命名 :: 核心注册数量 ] """

    TASK_SIGN_COUNT: str = 'task_sign_count'
    """ [ 常量 :: 运行环境表字段命名 :: 任务注册数量 ] """


class ConstDbConfigNaming(object):
    """
    [ 常量 :: 配置表字段命名 ]

    * NOT MESSAGE

    """

    ID: str = 'id'
    """ [ 常量 :: 配置表字段命名 :: 配置编号 ] """

    NAME: str = 'name'
    """ [ 常量 :: 配置表字段命名 :: 配置名称 ] """

    CORE_MAXSIZE: str = 'core_maxsize'
    """ [ 常量 :: 配置表字段命名 :: 核心最大值 ] """

    TASK_MAXSIZE: str = 'task_maxsize'
    """ [ 常量 :: 配置表字段命名 :: 任务最大值 ] """


class ConstDbTaskNaming(object):
    """
    [ 常量 :: 任务表字段命名 ]

    * NOT MESSAGE

    """

    TID: str = 'tid'
    """ [ 常量 :: 任务表字段命名 :: 任务编号 ] """

    NAME: str = 'name'
    """ [ 常量 :: 任务表字段命名 :: 任务名称 ] """

    REMARK: str = 'remark'
    """ [ 常量 :: 任务表字段命名 :: 任务备注信息 ] """

    CREATED_DATE: str = 'created_date'
    """ [ 常量 :: 任务表字段命名 :: 创建日期 ] """

    STATE: str = 'state'
    """ [ 常量 :: 任务表字段命名 :: 任务状态 ] """

    START_TIME: str = 'start_time'
    """ [ 常量 :: 任务表字段命名 :: 开始时间 ] """

    END_TIME: str = 'end_time'
    """ [ 常量 :: 任务表字段命名 :: 结束时间 ] """

    SPEND_TIME_S: str = 'spend_time_s'
    """ [ 常量 :: 任务表字段命名 :: 消耗时间(秒) ] """

    CASE_ALL: str = 'case_all'
    """ [ 常量 :: 任务表字段命名 :: 所有用例计数 ] """

    CASE_PASS: str = 'case_pass'
    """ [ 常量 :: 任务表字段命名 :: 成功的用例计数 ] """

    CASE_FAIL: str = 'case_fail'
    """ [ 常量 :: 任务表字段命名 :: 失败的用例计数 ] """


class ConstDbCaseNaming(object):
    """
    [ 常量 :: 用例表字段命名 ]

    * NOT MESSAGE

    """

    CID: str = 'cid'
    """ [ 常量 :: 用例表字段命名 :: 用例编号 ] """

    TID: str = 'tid'
    """ [ 常量 :: 用例表字段命名 :: 所属任务编号 ] """

    NAME: str = 'name'
    """ [ 常量 :: 用例表字段命名 :: 用例名称 ] """

    REMARK: str = 'remark'
    """ [ 常量 :: 用例表字段命名 :: 用例备注信息 ] """

    STATE: str = 'state'
    """ [ 常量 :: 用例表字段命名 :: 用例状态 ] """

    CREATED_DATE: str = 'created_date'
    """ [ 常量 :: 用例表字段命名 :: 创建日期 ] """

    START_TIME: str = 'start_time'
    """ [ 常量 :: 用例表字段命名 :: 开始时间 ] """

    END_TIME: str = 'end_time'
    """ [ 常量 :: 用例表字段命名 :: 结束时间 ] """

    SPEND_TIME_S: str = 'spend_time_s'
    """ [ 常量 :: 用例表字段命名 :: 消耗时间(秒) ] """

    RUN_STEP: str = 'run_step'
    """ [ 常量 :: 用例表字段命名 :: 运行步骤 ] """
