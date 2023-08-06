#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright 2022. quinn.7@foxmail.com All rights reserved.
# Author :: cat7
# Email  :: quinn.7@foxmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
[ Rains.DB.RainsDB ]

"""


import sqlite3
from threading import Lock

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD
from rains.baseic.decorator import singleton_pattern
from rains.baseic.error import RainsDbWriteError
from rains.baseic.error import RainsDbInitError
from rains.baseic.error import RainsDbReadError


# ----------------------------------
@singleton_pattern
class RainsDb(object):
    """
    [ Rains 数据库 ]

    * 基于 SQLite 数据库.

    """

    _conn: sqlite3.Connection = None
    """ [ 数据库连接对象 ] """

    _lock: Lock = Lock()
    """ [ 数据库互斥锁 ] """

    # ------------------------------
    def __init__(self):
        """
        [ Rains 数据库 ]

        """

        try:
            # 创建/连接数据库
            if not self._conn:
                self.connect()
                self._conn.commit()

        except BaseException as error:
            raise RainsDbInitError(error)

    # ------------------------------
    def read(self, sql: str) -> list:
        """
        [ 无锁读取 ]

        * 执行查询语句, 该函数不会持有数据库锁.

        ---
        参数:
            sql { str } : SQLite 查询语句.

        ---
        异常:
            RainsDbReadError : Rains 数据库读取异常.

        ---
        返回:
            list : 查询结果列表.

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

        except BaseException as error:
            raise RainsDbReadError(error)

    # ------------------------------
    def lock_read(self, sql: str) -> list:
        """
        [ 持锁读取 ]

        * 执行查询语句, 该函数会持有数据库锁, 结束时释放. 

        ---
        参数:
            sql { str } : SQLite 查询语句.

        ---
        异常:
            RainsDbReadError : Rains 数据库读取异常.

        ---
        返回:
            list : 查询结果列表.

        """

        # 获取锁
        with self._lock:

            # 执行读取函数
            return self.read(sql)

    # ------------------------------
    def write(self, sql: str) -> int:
        """
        [ 无锁写入 ]

        * 执行写入语句, 该函数不会持有数据库锁.

        ---
        参数:
            sql { str } : SQLite 查询语句.

        ---
        异常:
            RainsDbWriteError : Rains 数据库写入异常.

        ---
        返回:
            int : 写入数据后返回该条数据的自增ID.

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

        except BaseException as error:
            raise RainsDbWriteError(error)

    # ------------------------------
    def lock_write(self, sql: str) -> int:
        """
        [ 持锁写入 ]

        * 执行写入语句, 该函数会持有数据库锁, 结束时释放.

        ---
        参数:
            sql { str } : SQLite 查询语句.

        ---
        异常:
            RainsDbWriteError : Rains 数据库写入异常.

        ---
        返回:
            int : 写入数据后返回该条数据的自增ID.

        """

        # 获取锁
        with self._lock:

            # 执行写入函数
            return self.write(sql)

    # ------------------------------  
    def connect(self):
        """
        [ 数据库连接 ]

        """

        # 创建数据库连接对象
        self._conn = sqlite3.connect(CONST.SYS.PATH_DB_FILE, check_same_thread=False)

        # 创建数据库游标
        Cur = self._conn.cursor()

        # 构建数据库表
        for key, value in CreateTableSql.__dict__.items():
            if '__' in key:
                continue
            Cur.execute(value)

        # 注销数据库游标
        Cur.close()

    # ------------------------------
    def commit(self):
        """
        [ 事务保存 ]

        """

        self._conn.commit()

    # ------------------------------
    def rollback(self):
        """
        [ 事务回滚 ]

        """

        self._conn.rollback()

    # ------------------------------
    def quit(self):
        """
        [ 关闭数据库连接 ]

        """

        self._conn.close()


# ----------------------------------
class CreateTableSql(object):
    """
    [ 建表语句 ]

    """

    TASKS = f""" 

    CREATE TABLE IF NOT EXISTS { KEYWORD.DB.TASKS_TABLE }
    (
        { KEYWORD.ARG.TID }           INTEGER PRIMARY KEY, 
        { KEYWORD.ARG.NAME }          TEXT NOT NULL, 
        { KEYWORD.ARG.TYPE }          TEXT NOT NULL, 
        { KEYWORD.ARG.REMARK }        TEXT NOT NULL, 
        { KEYWORD.ARG.CREATED_DATE }  DATE NOT NULL, 
        { KEYWORD.ARG.STATE }         TEXT NOT NULL, 
        { KEYWORD.ARG.START_TIME }    DATE, 
        { KEYWORD.ARG.END_TIME }      DATE, 
        { KEYWORD.ARG.SPEND_TIME_S }  INT, 
        { KEYWORD.ARG.CASE_ALL }      INT, 
        { KEYWORD.ARG.CASE_PASS }     INT, 
        { KEYWORD.ARG.CASE_FAIL }     INT
    );

    """

    """
    [ 建表语句 :: 任务表 ]

    * 记录任务的执行信息.

    ---
    结构体:
        tid { int } : 任务编号, 自增的表主键.
        name { str } : 任务名称.
        remark { str } : 任务备注信息.
        created_date { date } : 创建日期.
        state { bool } : 任务状态.
        start_time { date } : 开始时间.
        end_time { date } : 结束时间.
        spend_time_s { date } : 消耗时间(秒).
        case_all { int } : 所有用例计数.
        case_pass { int } : 成功的用例计数.
        case_fail { int } : 失败用例数计数.

    """

    # ------------------------------
    CASES = f"""

    CREATE TABLE IF NOT EXISTS { KEYWORD.DB.CASES_TABLE }
    (
        { KEYWORD.ARG.CID }           INTEGER PRIMARY KEY, 
        { KEYWORD.ARG.TID }           INT NOT NULL, 
        { KEYWORD.ARG.NAME }          TEXT NOT NULL, 
        { KEYWORD.ARG.REMARK }        TEXT NOT NULL, 
        { KEYWORD.ARG.STATE }         TEXT NOT NULL, 
        { KEYWORD.ARG.CREATED_DATE }  DATE NOT NULL, 
        { KEYWORD.ARG.START_TIME }    DATE, 
        { KEYWORD.ARG.END_TIME }      DATE, 
        { KEYWORD.ARG.SPEND_TIME_S }  INTEGER, 
        { KEYWORD.ARG.RUN_STEP }      TEXT
    );
        
    """

    """
    [ 建表语句 :: 用例表 ]

    * 记录用例的执行信息.

    ---
    结构体:
        cid { int } : 用例编号, 自增的表主键.
        tid { int } : 所属的任务记录编号.
        name { str } : 用例名称.
        remark { str } : 用例备注信息.
        state { bool } : 任务状态.
        created_date { date } : 创建日期.
        start_time { date } : 开始时间.
        end_time { date } : 结束时间.
        spend_time_s { date } : 消耗时间(秒).
        run_step { str } : 运行步骤.
            
    """
