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
[ Rains.Kit.Web.Packaging.WebPlantElement ]

"""

import time
from typing import Any

from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.core.common.action_recorder import ACTION_RECORDER
from rains.baseic.tools import Regular

from rains.kit.web.packaging.web_element_structure import WebElementStructure


# ----------------------------------
class WebPlantElement(object):
    """
    [ Web元素控件 ]

    * 基于元素特征构建指向该元素的元素控件对象.

    """

    _web_driver: Any
    """ 引擎对象 """

    _element_structure: WebElementStructure
    """ 元素结构体 """

    # ------------------------------
    def __init__(self, web_driver: Any, element_structure: WebElementStructure):
        """
        [ Web元素控件 ]

        ---
        参数:
            web_driver { WebDriver } : Web引擎对象.
            element_structure { WebElementStructure } : Web元素结构体.

        """

        self._web_driver = web_driver
        self._element_structure = element_structure

    # ------------------------------
    @property
    def get(self):
        """
        [ Web元素控件'获取'相关函数 ]

        """

        return _WebPlantElementMapGet(self._web_driver, self._element_structure)

    # ------------------------------
    def _map_get(self):
        return self.get

    # ------------------------------
    @property
    def mouse(self):
        """
        [ Web元素控件'鼠标'相关函数 ]

        """

        return _WebPlantElementMapMouse(self._web_driver, self._element_structure)

    # ------------------------------
    def _map_mouse(self):
        return self.mouse

    # ------------------------------
    @property
    def input(self):
        """
        [ Web元素控件'输入框'相关函数 ]

        """

        return _WebPlantElementMapInput(self._web_driver, self._element_structure)

    # ------------------------------
    def _map_input(self):
        return self.input

    # ------------------------------
    @property
    def selector(self):
        """
        [ Web元素控件'下拉框'相关函数 ]

        """

        return _WebPlantElementMapSelector(self._web_driver, self._element_structure)

    # ------------------------------
    def _map_selector(self):
        return self.selector


# ----------------------------------
class _WebPlantElementMapBase(object):
    """
    [ Web元素控件映射基础类 ]

    """

    _web_driver: Any
    _handler: Any
    _driver_id: int
    _element_container: list
    _element_structure: WebElementStructure

    # ------------------------------
    def __init__(self, web_driver: Any, element_structure: WebElementStructure):
        """
        [ Web元素控件映射基础类 ]

        ---
        参数:
            web_driver { WebDriver } : Web引擎对象.
            element_structure { WebElementStructure } : Web元素结构体.

        """

        self._web_driver = web_driver
        self._handler = web_driver.base_driver
        self._driver_id = web_driver.driver_id
        self._element_structure = element_structure

    # ------------------------------
    def _analytical_elements(self, wait: int = 15, tolerance: bool = False) -> list:
        """
        [ 解析元素结构 ]

        * 每一次调用页面元素组件的方法时, 都会调用该函数, 以更新定位结果, 确认组件是否存在于当前页面中.

        ---
        参数:
            wait { int, optional } : 查找元素所等待的显式等待时长.
            tolerance { bool, optional } : 容错模式, 为 True 则表示定位不到元素也不报错, 返回空列表.

        ---
        返回:
            list : 元素列表容器.

        """

        self._element_container = \
            self._web_driver.find_handle.find(self._element_structure, wait, tolerance)

        return self._element_container

    # ------------------------------
    def _prepare(self, message: str, is_inquire: bool = True):
        message = ''.join([
            self._element_structure.page, '.', 
            self._element_structure.name, ' >> ', 
            message
        ])

        if is_inquire:
            self._element_container = self._analytical_elements()

        return message


# ----------------------------------
class _WebPlantElementMapGet(_WebPlantElementMapBase):
    """
    [ Web元素控件'获取'相关函数 ]

    """

    # ------------------------------
    def count(self) -> int:
        """
        [ 获取元素数量 ]

        * 定位元素并且返回元素数量.

        ---
        返回:
            int : 元素数量.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.count.__doc__))
            count = len(self._element_container)
            execution_step_record(self._driver_id, message, count)

            return count

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def text(self, eid: int = 0) -> str:
        """
        [ 获取文本 ]

        * 返回元素的 text 属性值.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        ---
        返回:
            str : 元素文本.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.text.__doc__))
            text = self._element_container[eid].text
            execution_step_record(self._driver_id, message, text)

            return text

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def value(self, eid: int = 0) -> str:
        """
        [ 获取值 ]

        * 返回元素的 value 属性值.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        ---
        返回:
            str : 元素的值.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.value.__doc__))
            value = self._element_container[eid].get_attribute('value')
            execution_step_record(self._driver_id, message, value)

            return value

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def exist(self, eid: int = 0, wait: int = 3) -> bool:
        """
        [ 检查控件是否存在 ]

        * 尝试在当前页面中定位控件, 在等待时间内未找到则返回 False.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.
            wait { int, optional } : 查找元素所等待的显式等待时长, 默认为 3.

        ---
        返回:
            bool : True or False.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.exist.__doc__), is_inquire=False)
            self._analytical_elements(wait=wait, tolerance=True)

            proof = False
            if len(self._element_container) >= (eid + 1):
                proof = True

            execution_step_record(self._driver_id, message, str(proof))

            return proof

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantElementMapMouse(_WebPlantElementMapBase):
    """
    [ Web元素控件'鼠标'相关函数 ]

    """

    # ------------------------------
    def tap(self, eid: int = 0):
        """
        [ 左键点击 ]

        * 模拟一次作用于 WebElement 对象上的鼠标左键单击操作.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.tap.__doc__))
            ActionChains(self._handler).click(self._element_container[eid]).perform()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def double_tap(self, eid: int = 0):
        """
        [ 左键双击 ]

        * 模拟一次作用于 WebElement 对象上的鼠标左键双击操作.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.double_tap.__doc__))
            ActionChains(self._handler).double_click(self._element_container[eid]).perform()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def long_tap(self, eid: int = 0, sleep: int = 2):
        """
        [ 左键长按 ]

        * 模拟一次作用于 WebElement 对象上的鼠标左键长按操作.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.
            sleep { int, optional } : 长按时长, 默认为 2 秒.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.long_tap.__doc__))
            ActionChains(self._handler).click_and_hold(self._element_container[eid]).perform()
            time.sleep(sleep)
            ActionChains(self._handler).release(self._element_container[eid]).perform()
            execution_step_record(self._driver_id, message, str(f'{ sleep } 秒'))

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def move_to(self, eid: int = 0):
        """
        [ 鼠标悬停 ]

        * 模拟一次作用于 WebElement 对象上的鼠标悬停操作.

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.move_to.__doc__))
            ActionChains(self._handler).move_to_element(self._element_container[eid]).perform()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantElementMapInput(_WebPlantElementMapBase):
    """
    [ Web元素控件'输入框'相关函数 ]

    """

    # ------------------------------
    def send(self, key: str, eid: int = 0):
        """
        [ 输入内容 ]

        * 输入内容, 一般指向 input 标签组件.

        ---
        参数:
            key { str } : 内容文本.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.send.__doc__))
            self._element_container[eid].clear()
            self._element_container[eid].send_keys(key)
            execution_step_record(self._driver_id, message, key)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def clear(self, eid: int = 0):
        """
        [ 清除内容 ]

        * 清除内容, 一般指向 input 标签组件. 

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.clear.__doc__))
            self._element_container[eid].clear()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantElementMapSelector(_WebPlantElementMapBase):
    """
    [ Web元素控件'下拉框'相关函数 ]

    """

    _select_handle: Select
    """ [ 下拉框处理器 ] """

    # ------------------------------
    def get_option_items(self, eid: int = 0) -> list:
        """
        [ 获取下拉框中所有的选项文本 ]

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        ---
        返回:
            list : 包含下拉框中所有的选项文本的列表.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.get_option_items.__doc__))
            self._init_select_handle(eid)

            texts = []
            option_list = self._select_handle.options
            for i in option_list:
                texts.append(i.text)

            execution_step_record(self._driver_id, message, str(texts))

            return texts

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def get_option_select_items(self, eid: int = 0) -> list:
        """
        [ 获取下拉框中所有的已选中选项文本 ]

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        ---
        返回:
            list : 包含下拉框中所有的已选中选项文本的列表.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.get_option_select_items.__doc__))
            self._init_select_handle(eid)

            texts = []
            option_list = self._select_handle.all_selected_options
            for i in option_list:
                texts.append(i.text)

            execution_step_record(self._driver_id, message, str(texts))

            return texts

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def get_option_current_item(self, eid: int = 0) -> str:
        """
        [ 获取下拉框中当前选择的首个选项文本 ]

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        ---
        返回:
            str : 下拉框中当前选择的首个选项文本.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.get_option_current_item.__doc__))
            self._init_select_handle(eid)
            text = self._select_handle.first_selected_option.text
            execution_step_record(self._driver_id, message, text)

            return text

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def select_by_index(self, index: int, eid: int = 0):
        """
        [ 下拉框中通过下标选择选项 ]

        ---
        参数:
            index { int } : 需要选中的选项下标.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.select_by_index.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_index(index)
            select_option_text = self._select_handle.first_selected_option.text
            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def select_by_value(self, value: str, eid: int = 0):
        """
        [ 下拉框中通过选项标签属性值选择 ]

        ---
        参数:
            value { str } : 需要选中的选项标签属性值.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.select_by_value.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_value(value)
            select_option_text = self._select_handle.first_selected_option.text
            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def select_by_text(self, text: str, eid: int = 0):
        """
        [ 下拉框中通过选项的文本选择 ]

        ---
        参数:
            text { str } : 需要选中的选项文本.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.select_by_text.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_visible_text(text)
            select_option_text = self._select_handle.first_selected_option.text
            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def deselect_all(self, eid: int = 0):
        """
        [ 下拉框中取消所有的已选中选项 ]

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.deselect_all.__doc__))
            self._init_select_handle(eid)
            self._select_handle.deselect_all()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def deselect_by_index(self, index: int, eid: int = 0):
        """
        [ 下拉框中通过下标取消已选中选项 ]

        ---
        参数:
            index { int } : 需要取消选中的选项下标.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.deselect_by_index.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_index(index)
            select_option_text =self._select_handle.first_selected_option.text 
            self._select_handle.deselect_by_index(index)

            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def deselect_by_value(self, value: str, eid: int = 0):
        """
        [ 下拉框中通过选项标签属性值取消已选中选项 ]

        ---
        参数:
            value { str } : 需要取消选中的选项标签属性值.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.deselect_by_value.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_value(value)
            select_option_text =self._select_handle.first_selected_option.text 
            self._select_handle.deselect_by_value(value)

            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def deselect_by_text(self, text: str, eid: int = 0):
        """
        [ 下拉框中通过选项标签属性值取消已选中选项 ]

        ---
        参数:
            text { str } : 需要取消选中的选项的文本.
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        try:
            message = self._prepare(Regular.get_function_doc_name(self.deselect_by_text.__doc__))
            self._init_select_handle(eid)
            self._select_handle.select_by_visible_text(text)
            select_option_text =self._select_handle.first_selected_option.text 
            self._select_handle.deselect_by_visible_text(text)

            execution_step_record(self._driver_id, message, select_option_text)

        except BaseException as error:
            raise WebPlantElementFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def _init_select_handle(self, eid):
        """
        [ 初始化下拉框处理器 ]

        ---
        参数:
            eid { int, optional } : 指定元素下标, 默认为 0.

        """

        self._select_handle = Select(self._element_container[eid])


# ----------------------------------
def execution_step_record(driver_id: int, message: str, join_message: str = None, level: str = 'info'):
    """
    [ 执行步骤记录 ]

    * 执行时, 将同步将信息传递给日志服务与用例记录器.

    ---
    参数:
        driver_id { int } : 核心ID.
        message { str } : 记录信息.
        join_message { str } : 拼接信息.

    """

    if join_message:
        message = ''.join([message, ' >> ', f'[{ str(join_message) }]'])

    ACTION_RECORDER.write(driver_id, message)

    if CONFIG.debug:
        LOG.map(level, f'Driver[{ driver_id }] >> { message }')


# ----------------------------------
class WebPlantElementFunctionRunError(Exception):
    """ [ Web元素控件函数执行异常 ] """
    
    def __init__(self, driver_id: int, message: str, error: Any):
        self.message = f'error :: { message } :: { error } !'
        self.err_name = Regular.get_function_doc_name(self.__doc__)
        execution_step_record(driver_id, message, level='error')
        
    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', self.message])
