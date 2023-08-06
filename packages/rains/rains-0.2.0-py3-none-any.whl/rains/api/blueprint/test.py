# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""

import random

from flask import jsonify
from flask import request

from rains.api.server_request_handler import *
from rains.baseic.rains_pool import RainsPool

from rains.kit.web import *


app_blueprint_test = Blueprint('test', __name__)
""" [ 用例蓝图 ] """


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


TASKS = []
for i in range(200):
    TASKS.append({
        'id': i,
        'name': f'任务名称很长阿-{i}',
        'remark': '虚假的任务注释也很长阿',
        'execute_date': '2021-12-12',
        'is_completed': '已完成',
        'start_time': '12:12',
        'end_time': '12:12',
        'spend_time_s': random.randint(20, 100)
    })


@app_blueprint_test.route('/test', methods=['GET'])
def test() -> Response:
    try:
        token = request.headers['Authorization']
        if token:
            for k, v in USERS.items():
                if token == v['token']:

                    # core = WebCore()
                    # plant = WebPlant(core.engine)
                    # plant.view.to_url('https://www.baidu.com/')
                    #
                    # plant.element(
                    #     page='百度首页',
                    #     name='搜索框',
                    #     by_key='xpath',
                    #     by_value='//*[@id="kw"]'
                    # ).input.send('rains nice!')
                    #
                    # plant.element(
                    #     page='百度首页',
                    #     name='百度一下button',
                    #     by_key='xpath',
                    #     by_value='//*[@id="su"]'
                    # ).mouse.tap()
                    #
                    # plant.engine.end()
                    # del core
                    # del plant

                    RainsPool(
                        cores=[WebCore()],
                        tasks=[TaskTest]
                    ).running()

                    return jsonify({
                        'code': 0,
                        'result': {'data': '脚本已经执行完毕！'},
                        'message': 'ok',
                        'type': 'success'
                    })

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


@app_blueprint_test.route('/api/login', methods=['POST'])
def login() -> Response:
    try:
        paras: dict = ServerRequestHandler.analysis_request_parameter('username', 'password')

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

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


@app_blueprint_test.route('/api/getUserInfo', methods=['GET'])
def get_user_info() -> Response:
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


@app_blueprint_test.route('/api/logout', methods=['GET'])
def logout() -> Response:
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

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


@app_blueprint_test.route('/api/table/getDemoList', methods=['GET'])
def table() -> Response:
    try:
        page = request.args.get('page')
        page_size = request.args.get('pageSize')
        token = request.headers['Authorization']
        number = int(page) * int(page_size)

        paras = {
            'page': page,
            'number': request.args.get('pageSize')
        }

        # 获取服务器数据
        db_r = DB.read(SQL.task.get_info_all(paras))
        task_all_count = DB.read(SQL.task.get_count_all())[0][0]
        r_task = []
        for t in db_r:
            task = {}
            task.update({'id': t[0]})
            task.update({'name': t[1]})
            task.update({'remark': t[2]})
            task.update({'execute_date': str(t[3])})
            task.update({'is_completed': t[4]})
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
                            # 'items': TASKS[number-int(page_size):number:],
                            'items': r_task,
                            'total': task_all_count
                        },
                        'message': 'ok',
                        'type': 'success'
                    })

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


class TaskTest(WebTask):
    """
    测试任务
    """
    user_input: WebElement
    password_input: WebElement
    login_button: WebElement
    create_button: WebElement

    def set_class_starting(self):
        self.user_input = self.plant.element(
            page='超管后台',
            name='邮箱输入框',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[1]/div/input'
        )

        self.password_input = self.plant.element(
            page='超管后台',
            name='密码输入框',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[2]/div/input'
        )

        self.login_button = self.plant.element(
            page='超管后台',
            name='Login按钮',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[4]/div/button'
        )

        self.create_button = self.plant.element(
            page='超管后台',
            name='登录成功判断元素',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div/div[1]/a'
        )

    def set_function_starting(self):
        self.plant.view.to_url('http://manage.dev-tea.cblink.net/')

    def case_01(self):
        """
        登录
        """
        self.user_input.input.send('admin@baocai.us')
        self.password_input.input.send('123456')
        self.login_button.mouse.tap()
        return self.create_button.get.in_page() is True
