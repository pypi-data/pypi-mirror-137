# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


__all__ = ['RainsServer']


import gc
import time
import psutil

from multiprocessing.dummy import Pool
from multiprocessing.dummy import Manager
from multiprocessing.dummy import Lock
from multiprocessing.dummy import Queue

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from rains.baseic.log import Log

from rains.api import rains_app
from rains.api import request
from rains.api import jsonify
from rains.api import URL_PREFIX
from rains.api import Blueprint
from rains.api import Response
from rains.api import ServerRequestHandler

from rains.kit.web import *


mgr = Manager()
CORE_QUEUE: Queue = mgr.Queue(maxsize=2)
TASK_QUEUE: Queue = mgr.Queue(maxsize=20)

CORE_QUEUE.put(WebCore())
CORE_QUEUE.put(WebCore())


# 任务接口蓝图
rains_blueprint = Blueprint('rains', __name__)


@rains_blueprint.route(f'{ URL_PREFIX }/rains/test', methods=['GET'])
def tasks() -> Response:
    """

    """
    
    TASK_QUEUE.put(TaskTest)

    return jsonify({
        'code': 0,
        'result': {
            'data': '[测试] 任务已接收',
        },
        'message': 'ok',
        'type': 'success'
    })


@rains_blueprint.route(f'{ URL_PREFIX  }/rains/run', methods=['POST'])
def get_user_info():
    try:
        paras: dict = ServerRequestHandler.analysis_request_parameter(keys=['name'])
        token = request.headers['Authorization']

        if paras['name'] == 'CBLINK':
            TASK_QUEUE.put(BdSearch)

        return jsonify({
            'code': 0,
            'result': {
                'data': f'[{ paras["name"] }] 任务已完成'
            },
            'message': 'ok',
            'type': 'success'
        })

    except BaseException as e:
        return ServerRequestHandler.unsuccessful(f'{ e }')


rains_app.register_blueprint(rains_blueprint)


class RainsServer(object):
    """
    [ Rains 服务 ]

    * 开启时，将在本地挂起一个 Rains 执行池进程与 RainsAPI 服务。

    """

    _log: Log = Log()
    """ [ 日志服务 ] """

    _pool: Pool
    """ [ 进程池 ] """

    _pool_state: bool
    """ [ 进程池运作状态 ] """

    _max_quantity_pool: int = 3
    """ [ 进程最大阈值 ] """

    _max_quantity_core: int = 5
    """ [ 核心最大阈值 ] """

    _max_quantity_task: int = 20
    """ [ 任务最大阈值 ] """

    _lock_from_core_queue: Lock
    """ [ 核心队列互斥锁 ] """

    _lock_from_task_queue: Lock
    """ [ 任务队列互斥锁 ] """

    _lock_from_pool_state: Lock
    """ [ 进程池运作状态互斥锁 ] """

    _lock_from_task_count: Lock
    """ [ 注册的任务数量互斥锁 ] """

    def __init__(self):
        """
        [ 运行池 ]

        * NOT MESSAGE

        """

        # 初始化赋值
        self._initialization()

    def _initialization(self):
        """
        [ 初始化进程池 ]

        * NOT MESSAGE

        """

        # 创建互斥锁
        self._lock_from_core_queue = mgr.Lock()
        self._lock_from_task_queue = mgr.Lock()
        self._lock_from_pool_state = mgr.Lock()
        self._lock_from_task_count = mgr.Lock()

        # 创建进程池
        self._pool = Pool(self._max_quantity_pool)

    def running(self):
        """
        [ 运行 ]

        * NOT MESSAGE

        """

        self._pool.apply_async(func=self.monitor)

        http_server = HTTPServer(WSGIContainer(rains_app))
        http_server.listen(3700)
        print('RainsAPI running...')
        IOLoop.current().start()

    def monitor(self):
        """
        [ 监听 ]

        * NOT MESSAGE

        """

        self._pool_state = True

        while True:

            time.sleep(3)
            print('监听周期开始')

            task = TASK_QUEUE.get()

            # 驱动冷启动时会占用大量的 CPU 资源，为避免因为 CPU 占用率过高导致进程启动异常
            # 每隔 2 秒检查 CPU 占用率，只有 CPU 占用率少于 50 时才会启动进程
            while True:
                if psutil.cpu_percent(2) < 50:
                    print('调用进程执行任务..')
                    self._pool.apply_async(func=self._emit, args=[task,])
                    break

    def _emit(self, task):
        """
        [ 触发工作流 ]

        * NOT MESSAGE

        """

        # 强制 GC 回收垃圾避免内存溢出
        gc.collect()

        # 取出队列中的核心与任务
        core = CORE_QUEUE.get()

        # 执行核心的 running 函数
        core.start_task(task)

        # 触发回调
        self._function_call_back()

        # 核心执行完任务后，放回核心队列等待
        with self._lock_from_core_queue:
            CORE_QUEUE.put(core)

    def _function_call_back(self):
        """
        [ 触发回调 ]

        * 该回调将消耗任务数量。

        """

        with self._lock_from_task_count:
            ...


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
            name='Login按钮',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div/div[1]/a'
        )

    def set_function_starting(self):
        self.plant.view.to_url('http://manage.dev-tea.cblink.net/')

    def case_01(self):
        """
        登录成功
        """
        self.user_input.input.send('admin@baocai.us')
        self.password_input.input.send('123456')
        self.login_button.mouse.tap()
        return self.create_button.get.in_page() is True


class BdSearch(WebTask):
    """
    测试任务
    """
    search_input: WebElement
    search_ok: WebElement

    def set_class_starting(self):
        self.search_input = self.plant.element(
            page='百度',
            name='搜索输入框',
            by_key=BY.XPATH,
            by_value='//*[@id="kw"]'
        )

        self.search_ok = self.plant.element(
            page='百度',
            name='搜索确认按钮',
            by_key=BY.XPATH,
            by_value='//*[@id="su"]'
        )

    def set_function_starting(self):
        self.plant.view.to_url('http://www.baidu.com/')

    def case_01(self):
        """
        搜索
        """
        self.search_input.input.send('CBLINK')
        self.search_ok.mouse.tap()
        time.sleep(2)
        return True
