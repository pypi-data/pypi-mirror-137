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
[ Rains.DB.Blueprint.SqlTask ]

"""

from rains.server.db.common import RainsDbParameterHandler

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD


# ----------------------------------
class SqlTask(object):
    """
    [ SQL语句 :: 任务相关 ]

    """

    @staticmethod
    def get_count_all() -> str:

        """
        [ 查询所有任务数量 ]
        
        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 
        
        SELECT COUNT({ KEYWORD.ARG.TID })
        
        FROM { KEYWORD.DB.TASKS_TABLE }
        
        """

    # ------------------------------
    @staticmethod
    def get_count_pass() -> str:
        """
        [ 查询全部通过的任务数量 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 
        
        SELECT COUNT({ KEYWORD.ARG.TID })

        FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.CASE_FAIL } == 0

        """

    # ------------------------------
    @staticmethod
    def get_count_fail() -> str:
        """
        [ 查询存在异常的任务数量 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        SELECT COUNT({ KEYWORD.ARG.TID })

        FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.CASE_FAIL } != 0

        """

    # ------------------------------
    @staticmethod
    def get_count_from_data(paras: dict) -> str:
        """
        [ 查询指定日期中的任务数量 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            created_date { str } : 创建日期.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        SELECT COUNT({ KEYWORD.ARG.TID })

        FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.CREATED_DATE } = '{ paras[KEYWORD.ARG.CREATED_DATE] }'

        """

    # ------------------------------
    @staticmethod
    def get_date_list() -> str:
        """
        [ 查询去重后的所有存在任务的日期列表 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        SELECT DISTINCT { KEYWORD.ARG.CREATED_DATE } 

        FROM { KEYWORD.DB.TASKS_TABLE }

        ORDER BY ID DESC

        """

    # ------------------------------
    @staticmethod
    def get_spend_time_all() -> str:
        """
        [ 查询所有任务的消耗时间 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        SELECT SUM({ KEYWORD.ARG.SPEND_TIME_S })

        FROM { KEYWORD.DB.TASKS_TABLE }

        """

    # ------------------------------
    @staticmethod
    def get_spend_time_from_data(paras: dict) -> str:
        """
        [ 查询指定日期中所有任务的消耗时间 ]
        
        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            created_date { str } : 创建日期.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        SELECT SUM({ KEYWORD.ARG.SPEND_TIME_S })

        FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.CREATED_DATE } = '{ paras[KEYWORD.ARG.CREATED_DATE] }'

        """

    # ------------------------------
    @staticmethod
    def get_info_all(
        page: int = 1,
        number: int = 10
    ) -> str:
        """
        [ 查询所有任务详情信息 ]

        ---
        参数:
            page { int } : 页数.
            number { int } : 单页数据量.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        SELECT * 

        FROM { KEYWORD.DB.TASKS_TABLE }

        ORDER BY { KEYWORD.ARG.TID } DESC 

        LIMIT { RainsDbParameterHandler.get_desc_limit(page, number) }

        """

    # ------------------------------
    @staticmethod
    def get_info_from_tid(paras: dict) -> str:
        """
        [ 查询指定TID的任务详情信息 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { int } : 任务编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        SELECT *

        FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.TID } = { paras[KEYWORD.ARG.TID] }

        """

    # ------------------------------
    @staticmethod
    def add(paras: dict) -> str:
        """
        [ 创建任务 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            name { str } : 任务名称.
            type { str } : 任务类型.
            remark { str } : 任务备注.
            created_date { str } : 创建日期.
            state { str } : 任务状态.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        INSERT INTO { KEYWORD.DB.TASKS_TABLE } (

             { KEYWORD.ARG.TID }, 
             { KEYWORD.ARG.NAME }, 
             { KEYWORD.ARG.TYPE }, 
             { KEYWORD.ARG.REMARK }, 
             { KEYWORD.ARG.CREATED_DATE }, 
             { KEYWORD.ARG.STATE }, 
             { KEYWORD.ARG.START_TIME }, 
             { KEYWORD.ARG.END_TIME }, 
             { KEYWORD.ARG.SPEND_TIME_S }, 
             { KEYWORD.ARG.CASE_ALL }, 
             { KEYWORD.ARG.CASE_PASS }, 
             { KEYWORD.ARG.CASE_FAIL }
        )

        VALUES (

            NULL, 
            '{ paras[KEYWORD.ARG.NAME] }', 
            '{ paras[KEYWORD.ARG.TYPE] }', 
            '{ paras[KEYWORD.ARG.REMARK] }', 
            '{ paras[KEYWORD.ARG.CREATED_DATE] }', 
            '{ paras[KEYWORD.ARG.STATE] }', 
            NULL, NULL, NULL, NULL, NULL, NULL
        )

        """

    # ------------------------------
    @staticmethod
    def update(paras: dict) -> str:
        """
        [ 更新任务 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { int } : 任务编号.
            state { str } : 任务状态.
            start_time { str } : 开始时间.
            end_time { str } : 结束时间.
            spend_time_s { int } : 消耗时间(秒).
            case_all { int } : 所有用例计数.
            case_pass { int } : 成功的用例计数.
            case_fail { int } : 失败用例数计数.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        UPDATE { KEYWORD.DB.TASKS_TABLE }

        SET
            { KEYWORD.ARG.STATE }  = '{ paras[KEYWORD.ARG.STATE] }', 
            { KEYWORD.ARG.START_TIME }    = '{ paras[KEYWORD.ARG.START_TIME] }', 
            { KEYWORD.ARG.END_TIME }      = '{ paras[KEYWORD.ARG.END_TIME] }', 
            { KEYWORD.ARG.SPEND_TIME_S }  = '{ paras[KEYWORD.ARG.SPEND_TIME_S] }', 
            { KEYWORD.ARG.CASE_ALL }      =  { paras[KEYWORD.ARG.CASE_ALL] }, 
            { KEYWORD.ARG.CASE_PASS }     =  { paras[KEYWORD.ARG.CASE_PASS] }, 
            { KEYWORD.ARG.CASE_FAIL }     =  { paras[KEYWORD.ARG.CASE_FAIL] }

        WHERE { KEYWORD.ARG.TID } = { paras[KEYWORD.ARG.TID] }

        """

    # ------------------------------
    @staticmethod
    def delete(paras: dict) -> str:
        """
        [ 删除任务 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { int } : 任务编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        DELETE FROM { KEYWORD.DB.TASKS_TABLE }

        WHERE { KEYWORD.ARG.TID } = { paras[KEYWORD.ARG.TID] }

        """

    # ------------------------------ 
    @staticmethod
    def delete_all() -> str:
        """
        [ 删除所有的任务 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        DELETE FROM { KEYWORD.DB.TASKS_TABLE }

        """
