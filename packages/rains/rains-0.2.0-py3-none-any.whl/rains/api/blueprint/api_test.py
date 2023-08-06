# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

from rains.api.server_request_handler import DB
from rains.api.server_request_handler import SQL
from rains.api.server_request_handler import URL_PREFIX
from rains.api.server_request_handler import jsonify
from rains.api.server_request_handler import request
from rains.api.server_request_handler import Blueprint
from rains.api.server_request_handler import ServerRequestHandler

from rains.baseic.log import Log


LOG: Log = Log()

# 测试接口蓝图
test_blueprint = Blueprint('test', __name__)

# 临时用户数据
USERS = {
    'admin': {
        'userId': 1,
        'username': 'admin',
        'realName': 'Rains Admin',
        'avatar': 'http://mms0.baidu.com/it/u=2163504278,3640533387&fm=253&app=138&f=JPEG&fmt=auto&q=75?w=500&h=707',
        'desc': 'manager',
        'password': 'admin',
        'token': 'fakeToken1',
        'homePath': '/dashboard/workbench',
        'roles': [
            {
                'roleName': 'Super Admin',
                'value': 'super'
            },
        ],
    }
}

@test_blueprint.route(f'{URL_PREFIX}/login', methods=['POST'])
def get() -> jsonify:
    try:
        paras: dict = ServerRequestHandler.analysis_request_parameter(keys=['username', 'password'])

        if paras['username'] in USERS.keys():
            user = USERS[paras['username']]
            if user['password'] == paras['password']:
                result = {
                    'roles': user['roles'],
                    'userId': user['userId'],
                    'username': user['username'],
                    'token': user['token'],
                    'realName': user['realName'],
                    'desc': user['desc'],
                }
                return jsonify({
                    'code': 0,
                    'result': result,
                    'message': 'ok',
                    'type': 'success'
                })
        else:
            return jsonify({
                'code': -1,
                'result': None,
                'message': 'Incorrect account or password！',
                'type': 'error'
            })

    except BaseException as err:
        return ServerRequestHandler.unsuccessful(f'{ err }')


@test_blueprint.route(f'{URL_PREFIX}/getUserInfo', methods=['GET'])
def get_user_info() -> jsonify:
    try:
        token = request.headers['Authorization']

        if token:
            for k, v in USERS.items():
                if token == v['token']:
                    return jsonify({
                        'code': 0,
                        'result': v,
                        'message': 'ok',
                        'type': 'success'
                    })

        else:
            return jsonify({
                'code': -1,
                'result': None,
                'message': 'Invalid token!',
                'type': 'error'
            })

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


@test_blueprint.route(f'{URL_PREFIX}/logout', methods=['GET'])
def logout() -> jsonify:
    try:
        token = request.headers['Authorization']

        if token:
            for k, v in USERS.items():
                if token == v['token']:
                    return jsonify({
                        'code': 0,
                        'result': v,
                        'message': 'Token has been destroyed',
                        'type': 'success'
                    })

        else:
            return jsonify({
                'code': -1,
                'result': None,
                'message': 'Invalid token!',
                'type': 'error'
            })

    except BaseException as err:
        return ServerRequestHandler.unsuccessful(f'{ err }')


@test_blueprint.route(f'{URL_PREFIX}/table/getDemoList', methods=['GET'])
def table() -> jsonify:
    try:
        page = request.args.get('page')
        page_size = request.args.get('pageSize')
        token = request.headers['Authorization']

        paras = {
            'page': page,
            'number': page_size
        }

        # 获取服务器数据
        db_r = DB.read(SQL.task.get_info_all(paras))
        task_all_count = DB.read(SQL.task.get_count_all())[0][0]
        r_task = []
        for t in db_r:
            task = {}
            task.update({'tid': t[0]})
            task.update({'name': t[1]})
            task.update({'remark': t[2]})
            task.update({'created_date': str(t[3])})
            task.update({'state': t[4]})
            task.update({'start_time': t[5]})
            task.update({'end_time': t[6]})
            task.update({'spend_time_s': t[7]})
            r_task.append(task)

        if token:
            for k, v in USERS.items():
                if token == v['token']:
                    return jsonify({
                        'code': 0,
                        'result': {
                            'items': r_task,
                            'total': task_all_count
                        },
                        'message': 'ok',
                        'type': 'success'
                    })

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')
