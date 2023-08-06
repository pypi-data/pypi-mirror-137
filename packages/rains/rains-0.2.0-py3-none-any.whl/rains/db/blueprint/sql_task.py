# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = ['SqlTask']


from rains.db.common import ConstDbTaskNaming
from rains.db.common import ConstDbCaseNaming
from rains.db.common import ConstDbTableNaming

from rains.db.common import RainsDbParameterHandler


CONST_TABLE = ConstDbTableNaming
CONST_TASK_NAMING = ConstDbTaskNaming
CONST_CASE_NAMING = ConstDbCaseNaming


class SqlTask(object):
    """
    [ SQL语句 :: 任务相关 ]

    * NOT MESSAGE

    """

    @staticmethod
    def get_count_all() -> str:
        """
        [ 查询所有任务数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 
        
        SELECT COUNT({ CONST_TASK_NAMING.TID })
        
        FROM { CONST_TABLE.TASKS }
        
        """

    @staticmethod
    def get_count_pass() -> str:
        """
        [ 查询全部通过的任务数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 
        
        SELECT COUNT({ CONST_TASK_NAMING.TID })

        FROM { CONST_TABLE.TASKS }

        WHERE { CONST_TASK_NAMING.CASE_FAIL } == 0

        """

    @staticmethod
    def get_count_fail() -> str:
        """
        [ 查询存在异常的任务数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_TASK_NAMING.TID })

        FROM { CONST_TABLE.TASKS }

        WHERE { CONST_TASK_NAMING.CASE_FAIL } != 0

        """

    @staticmethod
    def get_count_from_data(paras: dict) -> str:
        """
        [ 查询指定日期中的任务数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            created_date (str) : [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_TASK_NAMING.TID })

        FROM { CONST_TABLE.TASKS }

        WHERE { CONST_TASK_NAMING.CREATED_DATE } = '{ paras[CONST_TASK_NAMING.CREATED_DATE] }'

        """

    @staticmethod
    def get_date_list() -> str:
        """
        [ 查询去重后的所有存在任务的日期列表 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        SELECT DISTINCT { CONST_TASK_NAMING.CREATED_DATE } 

        FROM { CONST_TABLE.TASKS }

        ORDER BY ID DESC

        """

    @staticmethod
    def get_spend_time_all() -> str:
        """
        [ 查询所有任务的消耗时间 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT SUM({ CONST_TASK_NAMING.SPEND_TIME_S })

        FROM { CONST_TABLE.TASKS }

        """

    @staticmethod
    def get_spend_time_from_data(paras: dict) -> str:
        """
        [ 查询指定日期中所有任务的消耗时间 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            created_date (str) : [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT SUM({ CONST_TASK_NAMING.SPEND_TIME_S })

        FROM { CONST_TABLE.TASKS }

        WHERE { CONST_TASK_NAMING.CREATED_DATE } = '{ paras[CONST_TASK_NAMING.CREATED_DATE] }'

        """

    @staticmethod
    def get_info_all(paras: dict) -> str:
        """
        [ 查询所有任务详情信息 ]

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

        FROM { CONST_TABLE.TASKS }

        ORDER BY { CONST_TASK_NAMING.TID } DESC 

        LIMIT { RainsDbParameterHandler.get_desc_limit(paras) }

        """

    @staticmethod
    def get_info_from_tid(paras: dict) -> str:
        """
        [ 查询指定TID的任务详情信息 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 任务编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        SELECT *

        FROM { CONST_TABLE.TASKS }

        WHERE { ConstDbTaskNaming.TID } = { paras[ConstDbTaskNaming.TID] }

        """

    @staticmethod
    def add(paras: dict) -> str:
        """
        [ 创建任务 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            name (str): [ 任务名称 ]
            remark (str): [ 任务备注 ]
            created_date (str): [ 创建日期 ]
            state (str): [ 任务状态 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        INSERT INTO { CONST_TABLE.TASKS } (

             { CONST_TASK_NAMING.TID }, 
             { CONST_TASK_NAMING.NAME },
             { CONST_TASK_NAMING.REMARK },
             { CONST_TASK_NAMING.CREATED_DATE },
             { CONST_TASK_NAMING.STATE },
             { CONST_TASK_NAMING.START_TIME },
             { CONST_TASK_NAMING.END_TIME },
             { CONST_TASK_NAMING.SPEND_TIME_S },
             { CONST_TASK_NAMING.CASE_ALL },
             { CONST_TASK_NAMING.CASE_PASS },
             { CONST_TASK_NAMING.CASE_FAIL }
        )

        VALUES (

            NULL,
            '{ paras[CONST_TASK_NAMING.NAME] }',
            '{ paras[CONST_TASK_NAMING.REMARK] }',
            '{ paras[CONST_TASK_NAMING.CREATED_DATE] }',
            '{ paras[CONST_TASK_NAMING.STATE] }',
            NULL, NULL, NULL, NULL, NULL, NULL
        )

        """

    @staticmethod
    def update(paras: dict) -> str:
        """
        [ 更新任务 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 任务编号 ]
            state (str): [ 任务状态 ]
            start_time (str): [ 开始时间 ]
            end_time (str): [ 结束时间 ]
            spend_time_s (int): [ 消耗时间(秒) ]
            case_all (int): [ 所有用例计数 ]
            case_pass (int): [ 成功的用例计数 ]
            case_fail (int): [ 失败用例数计数 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        UPDATE { CONST_TABLE.TASKS }

        SET
            { CONST_TASK_NAMING.STATE }  = '{ paras[CONST_TASK_NAMING.STATE] }',
            { CONST_TASK_NAMING.START_TIME }    = '{ paras[CONST_TASK_NAMING.START_TIME] }',
            { CONST_TASK_NAMING.END_TIME }      = '{ paras[CONST_TASK_NAMING.END_TIME] }',
            { CONST_TASK_NAMING.SPEND_TIME_S }  = '{ paras[CONST_TASK_NAMING.SPEND_TIME_S] }',
            { CONST_TASK_NAMING.CASE_ALL }      =  { paras[CONST_TASK_NAMING.CASE_ALL] },
            { CONST_TASK_NAMING.CASE_PASS }     =  { paras[CONST_TASK_NAMING.CASE_PASS] },
            { CONST_TASK_NAMING.CASE_FAIL }     =  { paras[CONST_TASK_NAMING.CASE_FAIL] }

        WHERE { CONST_TASK_NAMING.TID } = { paras[CONST_TASK_NAMING.TID] }

        """

    @staticmethod
    def delete(paras: dict) -> str:
        """
        [ 删除任务 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 任务编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        DELETE FROM { CONST_TABLE.TASKS }

        WHERE ID = { paras[CONST_TASK_NAMING.TID] }

        """

    @staticmethod
    def delete_all() -> str:
        """
        [ 删除所有的任务 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        DELETE FROM { CONST_TABLE.TASKS }

        """
