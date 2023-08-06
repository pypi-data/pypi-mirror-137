# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


from rains.server.api.server_request_handler import *


app_blueprint_case = Blueprint('case', __name__)
""" [ 用例蓝图 ] """


@app_blueprint_case.route('/case/cases', methods=['POST'])
def cases() -> Response:
    """
    [ 获取用例列表 ]
    * 接收一个任务ID, 返回该任务的所有用例.

    [ 必要参数 ]
    * tid     (int) : 任务ID

    [ 可选参数 ]
    * state   (str) : 状态
    * page    (int) : 页数
    * number  (int) : 查询数量

    [ 返回内容 ]
    * Response 对象

    """

    try:
        # 解析请求参数
        paras: dict = ServerRequestHandler.analysis_request_parameter('tid', 'state', 'page', 'number')
        # 获取服务器数据
        base_case_list: list = DB.read(SQL.case.get_info_from_tid(paras))

        # 加工数据
        # 将用例信息中的运行步骤转换成列表然后重新拼接数据
        new_case_list: list = []
        for case_info in base_case_list:
            new_case_info: list = []
            number: int = 0
            for info in case_info:
                if number == 9:
                    info = info.split('\n')
                new_case_info.append(info)
                number += 1
            new_case_list.append(new_case_info)

        return ServerRequestHandler.successful({'tid': paras['tid'], 'cases': new_case_list})

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')
