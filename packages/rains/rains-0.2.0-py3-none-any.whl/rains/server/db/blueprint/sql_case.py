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
[ Rains.DB.Blueprint.SqlCase ]

"""

from rains.server.db.common import RainsDbParameterHandler

from rains.baseic.const import CONST
from rains.baseic.keyword import KEYWORD


# ----------------------------------
class SqlCase(object):
    """
    [ SQL语句 :: 用例相关 ]

    """

    # ------------------------------
    @staticmethod
    def get_count_all() -> str:
        """
        [ 查询所有用例数量 ]
        
        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """
        
        return f"""

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE }

        """

    # ------------------------------
    @staticmethod
    def get_count_pass() -> str:
        """
        [ 查询所有通过的用例数量 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """
        
        return f""" 

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE }

        WHERE { KEYWORD.ARG.STATE } == '{ CONST.STATE.END }'

        """

    # ------------------------------
    @staticmethod
    def get_count_fail() -> str:
        """
        [ 查询所有非'成功'的用例数量 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """
        
        return f""" 

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE }

        WHERE { KEYWORD.ARG.STATE } != '{ CONST.STATE.END }'

        """

    # ------------------------------
    @staticmethod
    def get_count_from_date(paras: dict) -> str:
        """
        [ 查询指定日期里所有用例数量 ]
        
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

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE }

        WHERE { KEYWORD.ARG.CREATED_DATE } == '{ paras[KEYWORD.ARG.CREATED_DATE] }'

        """

    # ------------------------------
    @staticmethod
    def get_count_fail_from_data(paras: dict) -> str:
        """
        [ 查询指定日期里所有非'成功'用例数量 ]

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

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE }

        WHERE { KEYWORD.ARG.STATE } != '{ CONST.STATE.END }'

        AND { KEYWORD.ARG.CREATED_DATE } == '{ paras[KEYWORD.ARG.CREATED_DATE] }'

        """

    # ------------------------------
    @staticmethod
    def get_count_from_tid(paras: dict) -> str:
        """
        [ 查询指定任务下所有用例数量 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { int } : 所属任务编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE } 

        WHERE { KEYWORD.ARG.TID } = { paras[KEYWORD.ARG.TID] }

        """

    # ------------------------------
    @staticmethod
    def get_count_form_date(paras: dict) -> str:
        """
        [ 查询指定执行日期的用例数量 ]

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

        SELECT COUNT({ KEYWORD.ARG.CID }) FROM { KEYWORD.DB.CASES_TABLE } 

        WHERE { KEYWORD.ARG.CREATED_DATE } = '{ paras[KEYWORD.ARG.CREATED_DATE] }'

        """

    # ------------------------------
    @staticmethod
    def get_info_from_tid(paras: dict) -> str:
        """
        [ 查询任务所有用例详情信息列表 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { str } : 所属任务编号.
            
        ---
        参数字典非必要参数:
            state { str } : 状态.
            page { int } : 页数.
            number { int } : 单页数据量.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        if KEYWORD.ARG.STATE in paras.keys():
            state = f'{ KEYWORD.ARG.STATE } = "{ paras[KEYWORD.ARG.STATE] }"'
        else:
            state = f'{ KEYWORD.ARG.STATE } in ("{ CONST.STATE.RUN }", ' \
                    f'"{ CONST.STATE.END }", "{ CONST.STATE.ERR }")'

        return f"""

        SELECT * FROM { KEYWORD.DB.CASES_TABLE }

        WHERE { state } AND { KEYWORD.ARG.TID } = { paras[KEYWORD.ARG.TID] }

        ORDER BY ID DESC

        LIMIT { RainsDbParameterHandler.get_desc_limit(paras) }

        """

    # ------------------------------
    @staticmethod
    def get_info_from_cid(paras: dict) -> str:
        """
        [ 查询指定编号用例详情信息列表 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            cid { int } : 用例编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        SELECT * FROM { KEYWORD.DB.CASES_TABLE }

        WHERE id = { paras[KEYWORD.ARG.CID] }

        """

    # ------------------------------
    @staticmethod
    def add(paras: dict) -> str:
        """
        [ 创建用例 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            tid { int } : 所属任务编号.
            name { str } : 用例名称.
            remark { str } : 用例备注信息.
            created_date { str } : 创建日期.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f""" 

        INSERT INTO { KEYWORD.DB.CASES_TABLE } (

            { KEYWORD.ARG.CID }, 
            { KEYWORD.ARG.TID }, 
            { KEYWORD.ARG.NAME }, 
            { KEYWORD.ARG.REMARK }, 
            { KEYWORD.ARG.STATE }, 
            { KEYWORD.ARG.CREATED_DATE }, 
            { KEYWORD.ARG.START_TIME }, 
            { KEYWORD.ARG.END_TIME }, 
            { KEYWORD.ARG.SPEND_TIME_S }, 
            { KEYWORD.ARG.RUN_STEP }
        )

        VALUES (

            NULL, 
            '{ paras[KEYWORD.ARG.TID] }', 
            '{ paras[KEYWORD.ARG.NAME] }', 
            '{ paras[KEYWORD.ARG.REMARK] }', 
            '{ CONST.STATE.RUN }', 
            '{ paras[KEYWORD.ARG.CREATED_DATE] }', 
             NULL, 
             NULL, 
             NULL, 
             NULL
        )

        """

    # ------------------------------
    @staticmethod
    def update(paras: dict) -> str:
        """
        [ 更新用例 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            cid { int } : 用例编号.
            state { str } : 用例状态.
            start_time { str } : 开始时间.
            end_time { str } : 结束时间.
            spend_time_s { str } : 消耗时间(秒).
            run_step { str } : 运行步骤.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        UPDATE { KEYWORD.DB.CASES_TABLE }

        SET 
            { KEYWORD.ARG.STATE }         = '{ paras[KEYWORD.ARG.STATE] }', 
            { KEYWORD.ARG.START_TIME }    = '{ paras[KEYWORD.ARG.START_TIME] }', 
            { KEYWORD.ARG.END_TIME }      = '{ paras[KEYWORD.ARG.END_TIME] }', 
            { KEYWORD.ARG.SPEND_TIME_S }  = '{ paras[KEYWORD.ARG.SPEND_TIME_S] }', 
            { KEYWORD.ARG.RUN_STEP }      = '{ paras[KEYWORD.ARG.RUN_STEP] }'

        WHERE
            { KEYWORD.ARG.CID } = { paras[KEYWORD.ARG.CID] }

        """

    # ------------------------------
    @staticmethod
    def delete_from_cid(paras: dict) -> str:
        """
        [ 删除指定用例 ]
        
        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            cid { int } : 用例编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        DELETE FROM { KEYWORD.DB.CASES_TABLE }

        WHERE ID = { paras[KEYWORD.ARG.CID] }

        """

    # ------------------------------
    @staticmethod
    def delete_from_tid(paras: dict = None) -> str:
        """
        [ 删除指定任务的所有用例 ]

        ---
        参数:
            paras { dict } : 参数字典.
            
        ---
        参数字典必要参数:
            cid { int } : 用例编号.

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        DELETE FROM { KEYWORD.DB.CASES_TABLE }

        WHERE TID = { paras[KEYWORD.ARG.TID] }

        """

    # ------------------------------
    @staticmethod
    def delete_all() -> str:
        """
        [ 删除所有用例 ]

        ---
        返回:
            str : 拼接完成的 SQLite 语句.

        """

        return f"""

        DELETE FROM { KEYWORD.DB.CASES_TABLE }

        """
