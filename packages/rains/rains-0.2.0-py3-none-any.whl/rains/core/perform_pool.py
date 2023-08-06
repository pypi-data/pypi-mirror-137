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
[ 执行池 ]

"""

import gc
import psutil
from typing import Any

from rains.baseic.log import LOG
from rains.core.common.pool_runtime import PoolRuntime
from rains.core.common.driver_agency import DriverAgency


# ----------------------------------
class PerFormPool(object):
    """
    [ 执行池 ]

    * 通常用于静态执行多进程任务.

    """

    _debug: bool
    """ [ 调试模式 ] """

    _config_runtime: PoolRuntime
    """ [ POOL运行时 ] """

    # ------------------------------
    def __init__(self, 
        debug: bool = False,
        driver_max_count: int = 3,
        task_max_count: int = 50
    ) -> None:
        """
        [ 执行池 ]

        ---
        参数:
            debug { bool, optional } : 调试模式.
            driver_max_count { int, optional } : 驱动最大数量.
            task_max_count { int, optional } : 任务最大数量.

        """

        self._debug = debug
        self._config_runtime = PoolRuntime(driver_max_count, task_max_count)

        # 创建驱动代理
        for _i in range(driver_max_count):
            self._config_runtime.driver_queue.put(DriverAgency())
            self._config_runtime.sign_driver()

    # ------------------------------
    def put_task(self, task: Any):
        """
        [ 推送到任务队列 ]
        
        ---
        参数:
            task { Any } : 任务对象.

        """

        count = self._config_runtime.task_queue.qsize()
        max_count = self._config_runtime.task_queue.maxsize
        if max_count > count:
            self._config_runtime.task_queue.put(task)

    # ------------------------------
    def running(self):
        """
        [ 运行 ]

        """

        # 开始一个监听循环
        while True:

            # 当 POOL运行时 任务队列为空 且 所有代理驱动都空闲时, 跳出监听循环
            if self._config_runtime.task_queue.qsize() == 0:
                if self._debug:
                    LOG.info('任务消耗完毕, 正在等待任务执行完毕.')
                while True:
                    core_count = self._config_runtime._driver_queue.qsize()
                    if core_count == self._config_runtime.sign_driver_count:
                        if self._debug:
                            LOG.info('任务全部执行完毕, 退出.')
                        break
                break

            task = self._config_runtime.task_queue.get()
            driver = self._config_runtime.driver_queue.get()

            # 驱动冷启动时会占用大量的 CPU 资源, 为避免因为 CPU 占用率过高导致进程启动异常
            # 每隔 2 秒检查 CPU 占用率, 只有 CPU 占用率少于 50 时才会启动进程
            while True:
                if psutil.cpu_percent(2) < 50:
                    self._config_runtime.pool.apply_async(func=self._emit, args=[task, driver])
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

        # 核心执行任务
        driver.start_task(task)

        # 核心执行完任务后, 放回核心队列等待
        self._config_runtime.driver_queue.put(driver)

        # 强制 GC 回收垃圾避免内存溢出
        gc.collect()
