# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

__all__ = ['SqlCase']


from rains.db.common import ConstDbTaskNaming
from rains.db.common import ConstDbCaseNaming
from rains.db.common import ConstDbTableNaming
from rains.db.common import ConstLifecycleState

from rains.db.common import RainsDbParameterHandler


CONST_TABLE = ConstDbTableNaming
CONST_TASK_NAMING = ConstDbTaskNaming
CONST_CASE_NAMING = ConstDbCaseNaming
CONST_LIFECYCLE_STATE = ConstLifecycleState


class SqlCase(object):
    """
    [ SQL语句 :: 用例相关 ]

    * NOT MESSAGE

    """

    @staticmethod
    def get_count_all() -> str:
        """
        [ 查询所有用例数量 ]

        * NOT MESSAGE

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """
        
        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES } 

        """

    @staticmethod
    def get_count_pass() -> str:
        """
        [ 查询所有通过的用例数量 ]

        * NOT MESSAGE

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """
        
        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES }

        WHERE { CONST_CASE_NAMING.STATE } == '{ CONST_LIFECYCLE_STATE.END }'

        """

    @staticmethod
    def get_count_fail() -> str:
        """
        [ 查询所有非'成功'的用例数量 ]

        * NOT MESSAGE

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """
        
        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES }

        WHERE { CONST_CASE_NAMING.STATE } != '{ CONST_LIFECYCLE_STATE.END }'

        """

    @staticmethod
    def get_count_from_date(paras: dict) -> str:
        """
        [ 查询指定日期里所有用例数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            created_date (str): [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES }

        WHERE { CONST_CASE_NAMING.CREATED_DATE } == '{ paras[CONST_CASE_NAMING.CREATED_DATE] }'

        """

    @staticmethod
    def get_count_fail_from_data(paras: dict) -> str:
        """
        [ 查询指定日期里所有非'成功'用例数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            created_date (str): [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES }

        WHERE { CONST_CASE_NAMING.STATE } != '{ CONST_LIFECYCLE_STATE.END }'

        AND { CONST_CASE_NAMING.CREATED_DATE } == '{ paras[CONST_CASE_NAMING.CREATED_DATE] }'

        """

    @staticmethod
    def get_count_from_tid(paras: dict) -> str:
        """
        [ 查询指定任务下所有用例数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 所属任务编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES } 

        WHERE { CONST_CASE_NAMING.TID } = { paras[CONST_CASE_NAMING.TID] }

        """

    @staticmethod
    def get_count_form_date(paras: dict) -> str:
        """
        [ 查询指定执行日期的用例数量 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            created_date (str): [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        SELECT COUNT({ CONST_CASE_NAMING.CID }) FROM { CONST_TABLE.CASES } 

        WHERE { CONST_CASE_NAMING.CREATED_DATE } = '{ paras[CONST_CASE_NAMING.CREATED_DATE] }'

        """

    @staticmethod
    def get_info_from_tid(paras: dict) -> str:
        """
        [ 查询任务所有用例详情信息列表 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 所属任务编号 ]

        ParasOptionKeys:
            state (str): [ 状态 ]
            page (int): [ 页数 ]
            number (int): [ 单页数据量 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        if CONST_CASE_NAMING.STATE in paras.keys():
            state = f'{ CONST_CASE_NAMING.STATE } = "{ paras[CONST_CASE_NAMING.STATE] }"'
        else:
            state = f'{ CONST_CASE_NAMING.STATE } in ("{ ConstLifecycleState.RUN }", ' \
                    f'"{ ConstLifecycleState.END }", "{ ConstLifecycleState.ERR }")'

        return f"""

        SELECT * FROM { CONST_TABLE.CASES }

        WHERE { state } AND { CONST_CASE_NAMING.TID } = { paras[CONST_CASE_NAMING.TID] }

        ORDER BY ID DESC

        LIMIT { RainsDbParameterHandler.get_desc_limit(paras) }

        """

    @staticmethod
    def get_info_from_cid(paras: dict) -> str:
        """
        [ 查询指定编号用例详情信息列表 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            cid (int): [ 用例编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        SELECT * FROM { CONST_TABLE.CASES }

        WHERE id = { paras[CONST_CASE_NAMING.CID] }

        """

    @staticmethod
    def add(paras: dict) -> str:
        """
        [ 创建用例 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 所属任务编号 ]
            name (str): [ 用例名称 ]
            remark (str): [ 用例备注信息 ]
            created_date (str): [ 创建日期 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f""" 

        INSERT INTO { CONST_TABLE.CASES } (

            { CONST_CASE_NAMING.CID }, 
            { CONST_CASE_NAMING.TID }, 
            { CONST_CASE_NAMING.NAME }, 
            { CONST_CASE_NAMING.REMARK }, 
            { CONST_CASE_NAMING.STATE }, 
            { CONST_CASE_NAMING.CREATED_DATE }, 
            { CONST_CASE_NAMING.START_TIME }, 
            { CONST_CASE_NAMING.END_TIME },
            { CONST_CASE_NAMING.SPEND_TIME_S },
            { CONST_CASE_NAMING.RUN_STEP }
        )

        VALUES (

            NULL,
            '{ paras[CONST_CASE_NAMING.TID] }',
            '{ paras[CONST_CASE_NAMING.NAME] }',
            '{ paras[CONST_CASE_NAMING.REMARK] }',
            '{ CONST_LIFECYCLE_STATE.RUN }', 
            '{ paras[CONST_CASE_NAMING.CREATED_DATE] }',
             NULL, 
             NULL,
             NULL,
             NULL
        )

        """

    @staticmethod
    def update(paras: dict) -> str:
        """
        [ 更新用例 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            cid (int): [ 用例编号 ]
            state (str): [ 用例状态 ]
            start_time (str): [ 开始时间 ]
            end_time (str): [ 结束时间 ]
            spend_time_s (str): [ 消耗时间(秒) ]
            run_step (str): [ 运行步骤 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        UPDATE { CONST_TABLE.CASES }

        SET 
            { CONST_CASE_NAMING.STATE }         = '{ paras[CONST_CASE_NAMING.STATE] }',
            { CONST_CASE_NAMING.START_TIME }    = '{ paras[CONST_CASE_NAMING.START_TIME] }',
            { CONST_CASE_NAMING.END_TIME }      = '{ paras[CONST_CASE_NAMING.END_TIME] }',
            { CONST_CASE_NAMING.SPEND_TIME_S }  = '{ paras[CONST_CASE_NAMING.SPEND_TIME_S] }',
            { CONST_CASE_NAMING.RUN_STEP }      = '{ paras[CONST_CASE_NAMING.RUN_STEP] }'

        WHERE
            { CONST_CASE_NAMING.CID } = { paras[CONST_CASE_NAMING.CID] }

        """

    @staticmethod
    def delete_from_cid(paras: dict) -> str:
        """
        [ 删除指定用例 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            cid (int): [ 用例编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        DELETE FROM { CONST_TABLE.CASES }

        WHERE ID = { paras[CONST_CASE_NAMING.CID] }

        """

    @staticmethod
    def delete_from_tid(paras: dict = None) -> str:
        """
        [ 删除指定任务的所有用例 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]
        
        ParasMustKeys:
            tid (int): [ 所属任务编号 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        DELETE FROM { CONST_TABLE.CASES }

        WHERE TID = { paras[CONST_CASE_NAMING.TID] }

        """

    @staticmethod
    def delete_all() -> str:
        """
        [ 删除所有用例 ]

        * NOT MESSAGE

        Args:
            paras (dict): [ 参数字典 ]

        Returns:
            str: [ 拼接完成的 SQLite 语句 ]

        """

        return f"""

        DELETE FROM { CONST_TABLE.CASES }

        """
