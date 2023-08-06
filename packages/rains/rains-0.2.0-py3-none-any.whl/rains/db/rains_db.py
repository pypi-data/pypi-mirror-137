# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

import sqlite3

from threading import Lock

from rains.const.const_file import ConstPath
from rains.db.rains_sql import RainsSql
from rains.const.const_db import ConstDbTaskNaming
from rains.const.const_db import ConstDbCaseNaming
from rains.const.const_db import ConstDbTableNaming
from rains.const.const_db import ConstDbConfigNaming
from rains.const.const_db import ConstDbRunEnvironmentNaming

from rains.baseic.decorator import singleton_pattern


@singleton_pattern
class RainsDb(object):
    """
    [ Rains 数据库 ]

    * 基于 SQLite 数据库。

    """

    _conn: sqlite3.Connection = None
    """ [ 数据库连接对象 ] """

    _lock: Lock = Lock()
    """ [ 数据库互斥锁 ] """

    def __init__(self):
        """
        [ Rains 数据库 ]

        * NOT MESSAGE

        """

        try:
            # 创建当前项目的日志目录
            if not ConstPath.DATA.is_dir():
                ConstPath.DATA.mkdir(parents=True, exist_ok=True)

            # 创建/连接数据库
            if not self._conn:
                self.connect()
                self._conn.commit()

        except BaseException as err:
            raise RainsDbInitError(str(err))

    def read(self, sql: str) -> list:
        """
        [ 无锁读取 ]

        * 执行查询语句，该函数不会持有数据库锁。

        Args:
            sql (str): [ SQLite 查询语句 ]

        Raises:
            RainsDbReadError: [ Rains 数据库读取异常 ]

        Returns:
            list: [ 查询结果列表 ]

        """

        try:
            # 创建数据库游标
            cur = self._conn.cursor()
            # 执行查询语句
            cur.execute(sql)
            # 获取查询结果
            data = cur.fetchall()
            # 注销数据库游标
            cur.close()

            return data

        except BaseException as err:
            raise RainsDbReadError(str(err))

    def lock_read(self, sql: str) -> list:
        """
        [ 持锁读取 ]

        * 执行查询语句，该函数会持有数据库锁，结束时释放。

        Args:
            sql (str): [ SQLite 查询语句 ]

        Raises:
            RainsDbReadError: [ Rains 数据库读取异常 ]

        Returns:
            list: [ 查询结果列表 ]

        """

        # 获取锁
        with self._lock:

            # 执行读取函数
            return self.read(sql)

    def write(self, sql: str) -> int:
        """
        [ 无锁写入 ]

        * 执行写入语句，该函数不会持有数据库锁。

        Args:
            sql (str): [ SQLite 语句 ]

        Raises:
            RainsDbWriteError: [ Rains 数据库写入异常 ]

        Returns:
            int: [ 写入数据后返回该条数据的自增ID ]

        """

        try:
            # 创建数据库游标
            cur = self._conn.cursor()
            # 执行查询语句
            cur.execute(sql)
            # 获取数据自增ID
            aid = cur.lastrowid
            # 注销数据库游标
            cur.close()

            return aid

        except BaseException as err:
            raise RainsDbWriteError(str(err))
    
    def lock_write(self, sql: str) -> int:
        """
        [ 持锁写入 ]

        * 执行写入语句，该函数会持有数据库锁，结束时释放。

        Args:
            sql (str): [ SQLite 语句 ]

        Raises:
            RainsDbWriteError: [ Rains 数据库写入异常 ]

        Returns:
            int: [ 写入数据后返回该条数据的自增ID ]
        """

        # 获取锁
        with self._lock:

            # 执行写入函数
            return self.write(sql)
        

    def connect(self):
        """
        [ 数据库连接 ]

        * NOT MESSAGE

        """

        # 创建数据库连接对象
        print(ConstPath.DATA_DB)
        self._conn = sqlite3.connect(ConstPath.DATA_DB, check_same_thread=False)
        # 创建数据库游标
        Cur = self._conn.cursor()

        # 构建数据库表
        for key, value in CreateTableSql.__dict__.items():
            if '__' in key:
                continue
            Cur.execute(value)

        # 清空运行环境表数据
        Cur.execute(f'DELETE FROM { ConstDbTableNaming.RUN_ENVIRONMENT }')
        Cur.execute(f'DELETE FROM { ConstDbTableNaming.CONFIG }')

        # 初始化运行环境表数据
        self.lock_write(RainsSql().run_environment.init())

        # 注销数据库游标
        Cur.close()

    def commit(self):
        """
        [ 事务保存 ]

        * NOT MESSAGE

        """

        self._conn.commit()

    def rollback(self):
        """
        [ 事务回滚 ]

        * NOT MESSAGE

        """

        self._conn.rollback()

    def quit(self):
        """
        [ 关闭数据库连接 ]

        * NOT MESSAGE

        """

        self._conn.close()


class CreateTableSql(object):
    """
    [ 建表语句 ]

    * NOT MESSAGE

    """

    RUN_ENVIRONMENT = f"""

    CREATE TABLE IF NOT EXISTS { ConstDbTableNaming.RUN_ENVIRONMENT }
    (
        id                                               INTEGER PRIMARY KEY,
        { ConstDbRunEnvironmentNaming.POOL_RUN_STATE }   BLOB NOT NULL,
        { ConstDbRunEnvironmentNaming.CORE_SIGN_COUNT }  INT NOT NULL,
        { ConstDbRunEnvironmentNaming.TASK_SIGN_COUNT }  INT NOT NULL
    );

    """

    """
    [ 建表语句 :: 运行环境表 ]

    * 记录当前的运行环境。

    Structure:
        id (int): 环境编号，自增的表主键
        pool_run_state (bool): 进程池运行状态
        core_sign_count (int): 核心注册数量
        task_sign_count (int): 任务注册数量

    """

    CONFIGS = f"""

    CREATE TABLE IF NOT EXISTS { ConstDbTableNaming.CONFIG }
    (
        { ConstDbConfigNaming.ID }            INTEGER PRIMARY KEY,
        { ConstDbConfigNaming.NAME }          TEXT NOT NULL,
        { ConstDbConfigNaming.CORE_MAXSIZE }  INT NOT NULL,
        { ConstDbConfigNaming.TASK_MAXSIZE }  INT NOT NULL
    );

    """

    """
    [ 建表语句 :: 配置表 ]

    * 记录配置信息。

    Structure:
        id (int): 配置编号，自增的表主键
        name (str): 配置名称
        core_maxsize (int): 核心最大值
        task_maxsize (int): 任务最大值

    """

    TASKS = f""" 

    CREATE TABLE IF NOT EXISTS { ConstDbTableNaming.TASKS }
    (
        { ConstDbTaskNaming.TID }           INTEGER PRIMARY KEY,
        { ConstDbTaskNaming.NAME }          TEXT NOT NULL,
        { ConstDbTaskNaming.REMARK }        TEXT NOT NULL,
        { ConstDbTaskNaming.CREATED_DATE }  DATE NOT NULL,
        { ConstDbTaskNaming.STATE }         TEXT NOT NULL,
        { ConstDbTaskNaming.START_TIME }    DATE,
        { ConstDbTaskNaming.END_TIME }      DATE,
        { ConstDbTaskNaming.SPEND_TIME_S }  INT,
        { ConstDbTaskNaming.CASE_ALL }      INT,
        { ConstDbTaskNaming.CASE_PASS }     INT,
        { ConstDbTaskNaming.CASE_FAIL }     INT
    );

    """

    """
    [ 建表语句 :: 任务表 ]

    * 记录任务的执行信息。

    Structure:
        tid (int): 任务编号，自增的表主键
        name (str): 任务名称
        remark (str): 任务备注信息
        created_date (date): 创建日期
        state (bool): 任务状态
        start_time (date): 开始时间
        end_time (date): 结束时间
        spend_time_s (date): 消耗时间(秒)
        case_all (int): 所有用例计数
        case_pass (int): 成功的用例计数
        case_fail (int): 失败用例数计数

    """

    CASES = f"""

    CREATE TABLE IF NOT EXISTS { ConstDbTableNaming.CASES }
    (
        { ConstDbCaseNaming.CID }           INTEGER PRIMARY KEY,
        { ConstDbCaseNaming.TID }           INT NOT NULL,
        { ConstDbCaseNaming.NAME }          TEXT NOT NULL,
        { ConstDbCaseNaming.REMARK }        TEXT NOT NULL,
        { ConstDbCaseNaming.STATE }         TEXT NOT NULL,
        { ConstDbCaseNaming.CREATED_DATE }  DATE NOT NULL,
        { ConstDbCaseNaming.START_TIME }    DATE,
        { ConstDbCaseNaming.END_TIME }      DATE,
        { ConstDbCaseNaming.SPEND_TIME_S }  INTEGER,
        { ConstDbCaseNaming.RUN_STEP }      TEXT
    );
        
    """

    """
    [ 建表语句 :: 用例表 ]

    * 记录用例的执行信息。
    
    Structure:
        cid (int): 用例编号，自增的表主键
        tid (int): 所属的任务记录编号
        name (str): 用例名称
        remark (str): 用例备注信息
        state (str): 用例状态
        created_date (date): 创建日期
        start_time (date): 开始时间
        end_time (date): 结束时间
        spend_time_s (date): 消耗时间(秒)
        run_step (str): 运行步骤
            
    """


class RainsDbInitError(Exception):

    def __init__(self, message: str):
        """
        [ Rains 数据库初始化异常 ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的错误信息 ]

        """

        self.message = message
    
    def __str__(self) -> str:
        
        return f"Rains 数据库初始化异常:: { self.message }"


class RainsDbReadError(Exception):

    def __init__(self, message: str):
        """
        [ Rains 数据库读取异常 ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的错误信息 ]

        """

        self.message = message
    
    def __str__(self) -> str:
        
        return f"Rains 数据库读取异常:: { self.message }"


class RainsDbWriteError(Exception):

    def __init__(self, message: str):
        """
        [ Rains 数据库写入异常 ]

        * NOT MESSAGE

        Args:
            message (str): [ 输出的错误信息 ]

        """

        self.message = message
    
    def __str__(self) -> str:
        
        return f"Rains 数据库写入异常:: { self.message }"
