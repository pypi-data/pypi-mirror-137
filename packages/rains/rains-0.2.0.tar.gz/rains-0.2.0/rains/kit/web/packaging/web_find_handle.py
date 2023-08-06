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
[ Rains.Kit.Web.Packaging.WebFindHandle ]

"""

from typing import Any

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import RemoteWebDriver

from rains.baseic.error import WebFindHandleFindElementError
from rains.kit.web.packaging.web_element_structure import WebElementStructure


# ----------------------------------
class WebFindHandle(object):
    """
    [ Web元素定位器 ]

    """

    _driver: RemoteWebDriver
    """ [ 原生驱动对象 ] """

    _web_driver_wait: WebDriverWait = WebDriverWait
    """ [ 原生驱动显示等待函数 ] """

    # ------------------------------
    def __init__(self, base_driver: RemoteWebDriver):
        """
        [ Web元素定位器 ]

        ---
        参数:
            base_driver { RemoteWebDriver } : Selenium 原生驱动对象.

        """

        self._driver = base_driver

    # ------------------------------
    def find(self, 
        element_structure: WebElementStructure, 
        wait: int = 15, 
        tolerance: bool = False
    ) -> list:
        """
        [ 元素定位 ]

        * 接受一个 WebElementStructure 对象, 并根据其描述从当前页面上定位元素列表.

        ---
        参数:
            element_structure { WebElementStructure } : 元素结构体.
            wait { int, optional } : 查找元素所等待的显式等待时长.
            tolerance { bool, optional } : 容错模式, 为 True 则表示定位不到元素也不报错, 返回空列表.

        ---
        返回:
            list : 已获取定位的元素列表.

        """

        # 解析元素搜索范围
        search_range = self._analysis_search_range(element_structure, wait)

        # 开始定位UI元素
        return self._base_explicitly_wait_find_element(
            by_key=element_structure.by_key, 
            by_value=element_structure.by_value, 
            driver=search_range, 
            wait=wait, 
            tolerance=tolerance
        )

    # ------------------------------
    def _analysis_search_range(self, element_structure: WebElementStructure, wait: int) -> Any:
        """
        [ 解析元素搜索范围 ]

        * 如果元素结构体中携带了锚元素则会返回定位的锚元素对象, 否则返回驱动. 

        ---
        参数:
            element_structure { WebElementStructure } : 元素结构体.
            wait { int } : 查找元素所等待的显式等待时长.

        ---
        返回:
            Any : 驱动 or 锚元素对象.

        """

        search_range = self._driver

        if element_structure.anchor_by_key:
            search_range = self._base_explicitly_wait_find_element(
                by_key=element_structure.anchor_by_key, 
                by_value=element_structure.anchor_by_value, 
                driver=search_range, 
                wait=wait, 
                tolerance=False
            )[element_structure.anchor_location_id]

        return search_range

    # ------------------------------
    def _base_explicitly_wait_find_element(self, 
                                           by_key: str, 
                                           by_value: str, 
                                           driver: RemoteWebDriver, 
                                           wait: int, 
                                           tolerance: bool) -> list:
        """
        [ 原生 WebDriverWait 封装 ]

        * 封装 WebDriverWait 全局显示等待获取函数.
        * 该函数将在每 0.5 秒时遍历一次页面, 直到找到元素或者等待(wait)超时. 
        * 如果容错开关(tolerance)为 True, 则表示定位不到元素时返回空列表.

        ---
        参数:
            by_key { str } : 元素定位策略.
            by_value { str } : 元素定位策略对应的值.
            driver { RemoteWebDriver } : Selenium 原生驱动对象.
            wait { int } : 查找元素所等待的显式等待时长.
            tolerance { bool } : 容错模式, 为 True 则表示定位不到元素也不报错, 返回空列表.

        ---
        异常:
            TimeoutException : 获取元素超时异常.
            WebFindHandleFindElementError : Web定位器获取元素异常.

        ---
        返回:
            list : 已获取定位的元素列表 or 空列表.

        """

        try:
            return self._web_driver_wait(driver, wait, poll_frequency=0.5, ignored_exceptions=None)\
                .until(ec.presence_of_all_elements_located((by_key, by_value)))

        except TimeoutException as error:
            # 触发异常时, 如果容错开关(tolerance)为 True, 则不抛出异常, 仅返回空列表
            if tolerance:
                return []
            else:
                raise WebFindHandleFindElementError(error)
