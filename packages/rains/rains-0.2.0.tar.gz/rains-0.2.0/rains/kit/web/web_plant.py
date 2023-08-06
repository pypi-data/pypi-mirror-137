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
[ Rains.Kit.Web.WebPlant ]

"""

from typing import Any

from selenium.webdriver.common.by import By

from rains.kit.web.packaging.web_plant_view import WebPlantView
from rains.kit.web.packaging.web_plant_element import WebPlantElement
from rains.kit.web.packaging.web_element_structure import WebElementStructure


BY: By = By
""" [ 元素定位策略 ] """


# ----------------------------------
class WebPlant(object):
    """
    [ Web 工厂构建类 ]

    * 工厂构建类提供了对浏览器视图与控件元素的封装.
    * 浏览器视图: 封装了浏览器本身的功能, 例如访问URL、管理标签页、控制弹窗、上传文件等.
    * 控件元素: 封装了对页面元素的操作功能, 如控制鼠标、控制输入框、下拉框、判断元素是否存在等.

    """

    _web_driver: Any
    """ [ Web 驱动程序 ] """

    # ------------------------------
    def __init__(self, web_driver: Any):
        """
        [ Web 工厂构建类 ]

        ---
        参数:
            web_driver { WebDriver } : Web 驱动程序.

        """

        self._web_driver = web_driver

    # ------------------------------
    @property
    def driver(self):
        return self._web_driver

    # ------------------------------
    @property
    def view(self) -> WebPlantView:
        """
        [ Web 视图 ]

        * 提供针对浏览器本身的操作函数, 例如访问URL, 最大化窗口, 截图PNG等等.

        ---
        返回:
            WebPlantView : Web 视图对象.

        """

        return WebPlantView(self._web_driver)

    # ------------------------------
    def _map_view(self):
        return self.view

    # ------------------------------
    def element(self, 
                page: str, 
                name: str, 
                by_key: str, 
                by_value: str, 
                anchor_by_key: str = None, 
                anchor_by_value: str = None, 
                anchor_location_id: int = None) -> WebPlantElement:
        """
        [ Web 元素控件 ]

        * 基于元素特征构建指向该元素的元素控件对象.
        * 元素控件对象封装了针对元素的一些操作元素, 例如鼠标点击、键盘输入等等. 
        
        ---
        参数:
            page { str } : 页面名称.
            name { str } : 组件名称.
            by_key { str } : 元素定位策略.
            by_value { str } : 元素定位策略对应的值.
            anchor_by_key { str, optional } : 锚点元素定位策略.
            anchor_by_value { str, optional } : 锚点元素定位策略对应的值.
            anchor_location_id { str, optional } : 锚点元素定位ID.

        ---
        返回:
            WebPlantElement : Web 元素控件对象.

        """

        element_structure = WebElementStructure(
            page, 
            name, 
            by_key, 
            by_value, 
            anchor_by_key, 
            anchor_by_value, 
            anchor_location_id
        )

        return WebPlantElement(self._web_driver, element_structure)
