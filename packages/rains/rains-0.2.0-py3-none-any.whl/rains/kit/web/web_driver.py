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
[ Rains.Kit.Web.WebDriver ]

"""

import random

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import RemoteWebDriver

from rains.baseic.const import CONST
from rains.baseic.interface.i_driver import IDriver
from rains.core.common.task_executor import TaskExecutor
from rains.kit.web.web_plant import WebPlant
from rains.kit.web.packaging.web_find_handle import WebFindHandle


WEB_DRIVER_SIGN_ID_LIST = []
""" [ 驱动程序编号池 ] """


# ----------------------------------
class WebDriver(IDriver):
    """
    [ Web 驱动程序 ]

    """
    
    _driver_id: int
    """ [ 驱动程序ID ] """

    _plant: WebPlant = None
    """ [ 构建工厂对象 ] """
    
    _state: bool = False
    """ [ 运行状态 ] """

    _task_executor: TaskExecutor
    """ [ 任务执行器 ] """
    
    _base_driver: RemoteWebDriver
    """ [ 原生驱动对象 ] """

    _find_handle: WebFindHandle
    """ [ 元素定位器 ] """

    _project_type: str = CONST.TYPE.PROJECT_TYPE_WEB
    """ [ 项目类型 ] """

    # ------------------------------
    def __init__(self):
        """
        [ Web 驱动程序 ]

        """

        # 生成随机ID并创建驱动程序
        while True:
            self._driver_id = random.randint(100, 999)

            if self._driver_id not in WEB_DRIVER_SIGN_ID_LIST:
                WEB_DRIVER_SIGN_ID_LIST.append(self._driver_id)
                break
            else:
                continue


        self._plant = WebPlant(self)
        self._task_executor = TaskExecutor(self)

    # ------------------------------
    def __enter__(self):
        """ 
        [ with enter ]

        * with 上下文实现.

        ---
        示例:
            >>> with WebDriver() as driver:
            >>>     driver.running()
            :: 执行完 with 内的语句后, 将执行 __exit__.
        
        """

        return self

    # ------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ 
        [ with exit ] 
        
        """

        self.end()

    # ------------------------------
    @property
    def plant(self):
        """
        [ 构建工厂 ]

        """

        return self._plant

    # ------------------------------
    @property
    def driver_id(self):
        """
        [ 驱动ID ]

        """

        return self._driver_id
    
    # ------------------------------
    @property
    def base_driver(self):
        """
        [ 原生驱动对象 ]

        """

        return self._base_driver
    
    # ------------------------------
    @property
    def find_handle(self):
        """
        [ 元素定位器 ]

        """

        return self._find_handle

    # ------------------------------
    @property
    def project_type(self):
        """
        [ 项目类型 ]

        """

        return self._project_type

    # ------------------------------
    def get_state(self) -> bool:
        """
        [ 获取引擎运行状态 ]

        * 获取引擎运行状态, 启动中返回 True, 否则返回 False. 

        Returns:
            bool: [ 引擎运行状态 ]

        """

        return self._state
    
    # ------------------------------
    def start_task(self, task):
        """
        [ 开始任务 ]

        * 接收一个 task, 并执行该 task.

        ---
        参数:
            task { Any } : 任务对象, 可以是实现 ITask 接口的任务类, 或者是 JSON 串译文.

        """

        self._task_executor.running(task)
        
        
    # ------------------------------
    def running(self, browser: str = 'CHROME'):
        """
        [ 运行引擎 ]

        * 驱动与定位器的实例化.

        """

        if not self._state:

            # 谷歌浏览器
            if browser == 'CHROME':

                # 创建浏览器驱动实例
                opt = webdriver.ChromeOptions()

                # 以非 W3C 模式运行
                opt.add_experimental_option('w3c', False)

                # 不显示自动化劫持 && 不打印日志
                opt.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])

                self._base_driver = webdriver.Chrome(options=opt)
                self._find_handle = WebFindHandle(self._base_driver)
                self._state = True

    # ------------------------------
    def end(self):
        """
        [ 结束引擎 ]

        * 退出并销毁当前持有的驱动与定位器. 

        """

        if self._state:

            self._base_driver.quit()
            self._state = False

            del self._base_driver
            del self._find_handle

    # ------------------------------
    def reset(self):
        """
        [ 重置引擎 ]

        * 将引擎重置至初始阶段.
        * 与 end() 相比, 该函数只是重置引擎至初始状态, 而不是注销.

        """

        if self._state:

            # 打开一个新空白标签页
            self._base_driver.execute_script(f'window.open("")')

            # 关闭所有其他标签页面
            new_page_handle = self._base_driver.window_handles[-1]

            for page_handle in self._base_driver.window_handles:
                if page_handle != new_page_handle:
                    self._base_driver.switch_to.window(page_handle)
                    self._base_driver.close()

            # 句柄回到新空白标签页
            self._base_driver.switch_to.window(new_page_handle)
