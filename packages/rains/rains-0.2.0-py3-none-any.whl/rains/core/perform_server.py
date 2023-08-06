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
[ 执行服务 ]

"""

import gc
import time
import psutil
from typing import Any

from flask import jsonify
from flask import Blueprint
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.server.api import RainsApp
from rains.server.api import URL_PREFIX
from rains.server.api import ServerRequestHandler
from rains.core.common.pool_runtime import PoolRuntime
from rains.core.common.driver_agency import DriverAgency

# ------------------------------
# 临时测试依赖
from rains.kit.web import WebTask
# ------------------------------


_POOL_RUNTIME: PoolRuntime = PoolRuntime()
""" [ POOL运行时 ] """

BLUEPRINT_RAINS = Blueprint('rains', __name__)
""" [ 任务接口蓝图 ] """


# 创建驱动代理
for _i in range(CONFIG.driver_max_count):
    _POOL_RUNTIME.driver_queue.put(DriverAgency())
    _POOL_RUNTIME.sign_driver()


# ------------------------------
# 临时测试依赖
@BLUEPRINT_RAINS.route(f'{ URL_PREFIX }/rains/test', methods=['GET'])
def tasks():
    
    _POOL_RUNTIME.task_queue.put(TaskTest)

    return jsonify({
        'code': 0, 
        'result': {
            'data': '[测试] 任务已接收', 
        }, 
        'message': 'ok', 
        'type': 'success'
    })
# ------------------------------


# ------------------------------
# 临时测试依赖
@BLUEPRINT_RAINS.route(f'{ URL_PREFIX }/rains/run', methods=['POST'])
def get_user_info():
    try:
        paras: dict = ServerRequestHandler.analysis_request_parameter(keys=['name'])

        if paras['name'] == 'BAIDU':
            _POOL_RUNTIME.task_queue.put(BdSearch)

        if paras['name'] == 'RAINS':
            _POOL_RUNTIME.task_queue.put(Rains)

        return jsonify({
            'code': 0, 
            'result': {
                'data': f'[{ paras["name"] }] 任务已完成'
            }, 
            'message': 'ok', 
            'type': 'success'
        })

    except BaseException as error:
        return ServerRequestHandler.unsuccessful(f'{ error }')
# ------------------------------


# ------------------------------
class PerformServer(object):
    """
    [ 执行服务 ]

    * 开启时, 将在本地挂起一个执行池进程与 WebAPI 服务.

    """

    # ------------------------------
    def __init__(self):
        """
        [ 执行服务 ]

        """
        ...

    # ------------------------------
    def running(self, port: int = 3700):
        """
        [ 运行 ]

        ---
        参数:
            port { int } : 服务端口号, 默认为 3700.

        """

        _POOL_RUNTIME.pool.apply_async(func=self.monitor)
        
        app = RainsApp()
        app.load_blueprint(BLUEPRINT_RAINS)
        
        http_server = HTTPServer(WSGIContainer(app.living))
        http_server.listen(port)

        LOG.info(f'执行服务运行中 >> 端口::[ { port } ] ')
        IOLoop.current().start()

    # ------------------------------
    def monitor(self):
        """
        [ 监听进程 ]

        * 监听来自 POOL运行时 的队列信息.

        """

        LOG.info('监听进程已启动...')

        while True:

            task = _POOL_RUNTIME.task_queue.get()
            driver = _POOL_RUNTIME.driver_queue.get()

            # 驱动冷启动时会占用大量的 CPU 资源, 为避免因为 CPU 占用率过高导致进程启动异常
            # 每隔 2 秒检查 CPU 占用率, 只有 CPU 占用率少于 50 时才会启动进程
            while True:
                if psutil.cpu_percent(2) < 50:
                    _POOL_RUNTIME.pool.apply_async(func=self._emit, args=[task, driver])
                    break

    # ------------------------------
    def _emit(self, task: Any, driver: Any):
        """
        [ 触发工作流 ]

        ---
        参数:
            task { Any } : 任务对象.
            driver { Any } : 驱动对象.

        """

        # 驱动执行任务
        driver.start_task(task)

        # 驱动执行完任务后, 放回核心队列等待
        _POOL_RUNTIME.driver_queue.put(driver)

        # 强制 GC 回收垃圾避免内存溢出
        gc.collect()



# ------------------------------
# 临时测试依赖
class TaskTest(WebTask):
    """
    测试任务
    """

    def set_task_init(self):

        print('任务 :: 执行任务起点函数')
        
        self.user_input = self.plant.element(
            page='超管后台', 
            name='邮箱输入框', 
            by_key='xpath', 
            by_value='/html/body/div/div/div/div/div[2]/form/div[1]/div/input'
        )

        self.password_input = self.plant.element(
            page='超管后台', 
            name='密码输入框', 
            by_key='xpath', 
            by_value='/html/body/div/div/div/div/div[2]/form/div[2]/div/input'
        )

        self.login_button = self.plant.element(
            page='超管后台', 
            name='Login按钮', 
            by_key='xpath', 
            by_value='/html/body/div/div/div/div/div[2]/form/div[4]/div/button'
        )

        self.create_button = self.plant.element(
            page='超管后台', 
            name='Login按钮', 
            by_key='xpath', 
            by_value='/html/body/div/div/div/div/div/div[1]/a'
        )

    def set_task_quit(self):
        print('任务 :: 执行任务终点函数')

    def set_case_init(self):
        print('任务 :: 执行用例起点函数')
        self.plant.view.page.goto('http://manage.dev-tea.cblink.net/')

    def set_case_quit(self):
        print('任务 :: 执行用例终点函数')

    def case_1(self):
        """
        登录成功
        """
        self.user_input.input.send('admin@baocai.us')
        self.password_input.input.send('123456')
        self.login_button.mouse.tap()
        return self.create_button.get.exist() is True
# ------------------------------


# ------------------------------
# 临时测试依赖
class BdSearch(WebTask):
    """
    示例: 百度搜索 CBLINK
    """

    def set_task_init(self):
        self.search_input = self.plant.element(
            page='百度', 
            name='搜索输入框', 
            by_key='xpath', 
            by_value='//*[@id="kw"]'
        )

        self.search_ok = self.plant.element(
            page='百度', 
            name='搜索确认按钮', 
            by_key='xpath', 
            by_value='//*[@id="su"]'
        )

    def set_case_init(self):
        self.plant.view.page.goto('http://www.baidu.com/')

    def case_01(self):
        self.search_input.input.send('CBLINK')
        self.search_ok.mouse.tap()
        time.sleep(2)
        return True
# ------------------------------


# ------------------------------
# 临时测试依赖
class Rains(WebTask):
    """
    示例: 登录 Rains-Admin 执行脚本
    """

    def set_task_init(self):
        self.user_input = self.plant.element(
            page='Rains', 
            name='账号输入框', 
            by_key='xpath', 
            by_value='//*[@id="account"]'
        )

        self.pasword_input = self.plant.element(
            page='Rains', 
            name='密码输入框', 
            by_key='xpath', 
            by_value='//*[@id="password"]'
        )

        self.login_button = self.plant.element(
            page='Rains', 
            name='登录按钮', 
            by_key='xpath', 
            by_value='//*[@id="app"]/div/div[2]/div/div[2]/div/form/div[4]/div/div/div/button/span'
        )

        self.to_test_home_button = self.plant.element(
            page='Rains', 
            name='跳转联调', 
            by_key='xpath', 
            by_value='//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/span'
        )

        self.click_running_button = self.plant.element(
            page='Rains', 
            name='点击执行脚本', 
            by_key='xpath', 
            by_value='//*[@id="app"]/section/section/section/div[3]/div/div[2]/button[1]/span'
        )

    def set_case_init(self):
        self.plant.view.set.browser_max()
        self.plant.view.page.goto('http://127.0.0.1:9001/')

    def case_01(self):
        self.user_input.input.send('admin')
        self.pasword_input.input.send('admin')
        self.login_button.mouse.tap()
        self.to_test_home_button.mouse.tap()
        self.click_running_button.mouse.tap()
        time.sleep(2)
        return True
# ------------------------------
