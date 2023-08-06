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
[ Rains.Kit.Web.Packaging.WebPlantView ]

"""

from typing import Any

from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import InvalidArgumentException

from rains.baseic.log import LOG
from rains.baseic.config import CONFIG
from rains.baseic.tools import Regular
from rains.core.common.action_recorder import ACTION_RECORDER
        

# ----------------------------------
class WebPlantView(object):
    """
    [ Web视图 ]

    * 提供针对浏览器本身的操作函数.

    """

    _web_driver: Any
    """ [ 引擎对象 ] """

    # ------------------------------
    def __init__(self, driver: Any):
        """
        [ Web视图 ]

        ---
        参数:
            driver { WebEngine } : Web引擎对象.

        """

        self._web_driver = driver

    # ------------------------------
    @property
    def get(self):
        """
        [ Web视图'获取'相关函数 ]

        """

        return _WebPlantViewMapGet(self._web_driver)

    # ------------------------------
    def _map_get(self):
        return self.get

    # ------------------------------
    @property
    def set(self):
        """
        [ Web视图'设置'相关函数 ]

        """

        return _WebPlantViewMapSet(self._web_driver)

    # ------------------------------
    def _map_set(self):
        return self.set

    # ------------------------------
    @property
    def page(self):
        """
        [ Web视图'页面'相关函数 ]

        """

        return _WebPlantViewMapPage(self._web_driver)

    # ------------------------------
    def _map_page(self):
        return self.page

    # ------------------------------
    @property
    def alert(self):
        """
        [ Web视图'弹窗'相关函数 ]

        """

        return _WebPlantViewMapAlert(self._web_driver)

    # ------------------------------
    def _map_alert(self):
        return self.alert


# ----------------------------------
class _WebPlantViewMapBase(object):
    """
    [ Web视图映射基础类 ]

    """

    _handler: Any
    _driver_id: int

    # ------------------------------
    def __init__(self, web_driver: Any):
        """
        [ Web视图映射基础类 ]

        ---
        参数:
            web_driver { WebDriver } : Web驱动对象.

        """

        self._handler = web_driver.base_driver
        self._driver_id = web_driver.driver_id


# ----------------------------------
class _WebPlantViewMapGet(_WebPlantViewMapBase):
    """
    [ Web视图'获取'相关函数 ]

    """

    # ------------------------------
    def url(self) -> str:
        """
        [ 获取当前标签页的 URL ]

        ---
        返回:
            str : 当前标签页的 URL 地址.

        """

        try:
            message = Regular.get_function_doc_name(self.url.__doc__)
            current_url = self._handler.current_url
            execution_step_record(self._driver_id, message, current_url)

            return current_url

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def title(self) -> str:
        """
        [ 获取当前标签页的 Title ]

        ---
        返回:
            str : 当前标签页的 Title 名称.

        """

        try:
            message = Regular.get_function_doc_name(self.title.__doc__)
            current_title = self._handler.title
            execution_step_record(self._driver_id, message, current_title)

            return current_title

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def window_list(self) -> Any:
        """
        [ 获取标签页句柄列表 ]

        ---
        返回:
            Any : 标签页句柄列表.

        """

        try:
            message = Regular.get_function_doc_name(self.window_list.__doc__)
            window_handles = self._handler.window_handles
            execution_step_record(self._driver_id, message, f'len:{ len(window_handles) }')

            return window_handles

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def window_current(self) -> Any:
        """
        [ 获取当前标签页句柄 ]

        ---
        返回:
            Any : 当前标签页句柄.

        """

        try:
            message = Regular.get_function_doc_name(self.window_current.__doc__)
            current_window_handle = self._handler.current_window_handle
            execution_step_record(self._driver_id, message, current_window_handle)

            return current_window_handle

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def browser_size(self) -> dict:
        """
        [ 获取浏览器尺寸 ]

        ---
        返回:
            dict : 标识浏览器尺寸信息的字典.

        """

        try:
            message = Regular.get_function_doc_name(self.browser_size.__doc__)
            browser_size = self._handler.get_window_size()
            execution_step_record(self._driver_id, message, browser_size)

            return browser_size

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def browser_position(self) -> dict:
        """
        [ 获取浏览器位置坐标 ]
        
        ---
        返回:
            dict : 标识浏览器位置坐标信息的字典.

        """

        try:
            message = Regular.get_function_doc_name(self.browser_position.__doc__)
            browser_position = self._handler.get_window_position()
            execution_step_record(self._driver_id, message, browser_position)

            return browser_position

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def cookies(self) -> list:
        """
        [ 获取 Cookies ]
        
        ---
        返回:
            list : Cookies 列表.

        """

        try:
            message = Regular.get_function_doc_name(self.cookies.__doc__)
            cookies = self._handler.get_cookies()
            execution_step_record(self._driver_id, message, len(cookies))

            return cookies

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantViewMapSet(_WebPlantViewMapBase):
    """
    [ WEB视图'设置'相关函数 ]

    """

    # ------------------------------
    def browser_size(self, width: int, height: int):
        """
        [ 设置浏览器尺寸 ]

        ---
        参数:
            width { int } : 宽度.
            height { int } : 高度.

        """

        try:
            message = Regular.get_function_doc_name(self.browser_size.__doc__)
            self._handler.set_window_size(width, height)
            execution_step_record(self._driver_id, message, {'width': width, 'height': height})

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def browser_position(self, x: int, y: int):
        """
        [ 设置浏览器位置坐标 ]

        ---
        参数:
            x { int } : x坐标.
            y { int } : y坐标.

        """

        try:
            message = Regular.get_function_doc_name(self.browser_position.__doc__)
            self._handler.set_window_position(x, y)
            execution_step_record(self._driver_id, message, {'x': x, 'y': y})

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def browser_max(self):
        """
        [ 设置浏览器窗口最大化 ]

        """

        try:
            message = Regular.get_function_doc_name(self.browser_max.__doc__)
            self._handler.maximize_window()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def browser_min(self):
        """
        [ 设置浏览器窗口最小化 ]

        """

        try:
            message = Regular.get_function_doc_name(self.browser_min.__doc__)
            self._handler.minimize_window()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def del_cookies(self):
        """
        [ 删除所有 Cookies ]

        """

        try:
            message = Regular.get_function_doc_name(self.del_cookies.__doc__)
            self._handler.delete_all_cookies()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def add_cookies(self, cookie_list: list):
        """
        [ 添加 Cookies ]

        ---
        参数:
            cookie_list { list } : Cookies 列表.

        """

        try:
            message = Regular.get_function_doc_name(self.add_cookies.__doc__)

            for cookie in cookie_list:
                self._handler.add_cookie(cookie)
            execution_step_record(self._driver_id, message, len(cookie_list))

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantViewMapPage(_WebPlantViewMapBase):
    """
    [ Web视图'页面'相关函数 ]

    """

    # ------------------------------
    def goto(self, url: str):
        """
        [ 跳转URL ]

        * 当前标签页跳转URL.

        ---
        参数:
            url { str } : URL.

        """

        try:
            message = Regular.get_function_doc_name(self.goto.__doc__)
            self._handler.get(url)
            execution_step_record(self._driver_id, message, url)

        except InvalidArgumentException:
            raise WebPlantViewFunctionRunError(self._driver_id, message, 'URL路径格式错误')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def refresh(self):
        """
        [ 刷新页面 ]

        * 当前标签页刷新页面.

        """

        try:
            message = Regular.get_function_doc_name(self.refresh.__doc__)
            self._handler.refresh()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def back(self):
        """
        [ 回退页面 ]

        * 当前标签页回退页面.

        """

        try:
            message = Regular.get_function_doc_name(self.back.__doc__)
            self._handler.back()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def forward(self):
        """
        [ 前滚页面 ]

        * 当前标签页前滚页面.

        """

        try:
            message = Regular.get_function_doc_name(self.forward.__doc__)
            self._handler.forward()
            execution_step_record(self._driver_id, message)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def save_png(self, save_path: str):
        """
        [ 保存快照 ]

        * 将当前浏览器截图保存至 save_path 中.

        ---
        参数:
            save_path { str } : 快照的完整保存路径.

        """

        try:
            message = Regular.get_function_doc_name(self.save_png.__doc__)
            self._handler.get_screenshot_as_file(str(save_path))
            execution_step_record(self._driver_id, message, save_path)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def window_open(self, url: str = ''):
        """
        [ 打开标签页 ]

        * 在当前浏览器中, 打开一个新的标签页.

        ---
        参数:
            url { str } : 新标签页的URL, 默认为空.

        """

        try:
            message = Regular.get_function_doc_name(self.window_open.__doc__)
            self._handler.execute_script(f'window.open("{url}")')
            self._handler.switch_to.window(self._handler.window_handles[-1])
            execution_step_record(self._driver_id, message, url)

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def window_goto(self, window_id: int):
        """
        [ 切换标签页 ]

        * 在当前浏览器中, 切换至编号为 [window_id] 的标签页.

        ---
        参数:
            window_id { int } : 标签页编号.

        """

        try:
            message = Regular.get_function_doc_name(self.window_goto.__doc__)
            self._handler.switch_to.window(self._handler.window_handles[window_id])
            execution_step_record(self._driver_id, message, self._handler.current_url)

        except IndexError:
            raise WebPlantViewFunctionRunError(self._driver_id, message, '标签页编号不存在')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def window_close(self, window_id: int):
        """
        [ 关闭标签页 ]

        * 在当前浏览器中, 关闭编号为 [window_id] 的已存在标签页.

        ---
        参数:
            window_id { int } : 标签页编号.

        """

        try:
            message = Regular.get_function_doc_name(self.window_close.__doc__)
            self._handler.switch_to.window(self._handler.window_handles[window_id])
            current_url = self._handler.current_url
            self._handler.close()
            self._handler.switch_to.window(self._handler.window_handles[0])
            execution_step_record(self._driver_id, message, current_url)

        except IndexError:
            raise WebPlantViewFunctionRunError(self._driver_id, message, '标签页编号不存在')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)


# ----------------------------------
class _WebPlantViewMapAlert(_WebPlantViewMapBase):
    """
    [ Web视图'弹窗'相关函数 ]

    """

    # ------------------------------
    def exist(self) -> bool:
        """
        [ 检查弹窗是否存在 ]

        ---
        返回:
            bool : True or False.

        """

        try:
            message = Regular.get_function_doc_name(self.exist.__doc__)
            is_exist = True

            try:
                self._handler.switch_to.alert
            except NoAlertPresentException:
                is_exist = False

            execution_step_record(self._driver_id, message, str(is_exist))

            return is_exist

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def text(self) -> str:
        """
        [ 获取弹窗文本 ]

        ---
        返回:
            str : 弹窗文本字符串.

        """

        try:
            message = Regular.get_function_doc_name(self.text.__doc__)
            alert_text = self._handler.switch_to.alert.text
            execution_step_record(self._driver_id, message, alert_text)

            return alert_text

        except NoAlertPresentException:
            raise WebPlantViewFunctionRunError(self._driver_id, message, '当前没有弹窗')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def tap_accept(self):
        """
        [ 点击弹窗确定按钮 ]

        """

        try:
            message = Regular.get_function_doc_name(self.tap_accept.__doc__)
            self._handler.switch_to.alert.accept()
            execution_step_record(self._driver_id, message)

        except NoAlertPresentException:
            raise WebPlantViewFunctionRunError(self._driver_id, message, '当前没有弹窗')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # ------------------------------
    def tap_dismiss(self):
        """
        [ 点击弹窗取消按钮 ]

        """
        
        try:
            message = Regular.get_function_doc_name(self.tap_dismiss.__doc__)
            self._handler.switch_to.alert.dismiss()
            execution_step_record(self._driver_id, message)

        except NoAlertPresentException:
            raise WebPlantViewFunctionRunError(self._driver_id, message, '当前没有弹窗')

        except BaseException as error:
            raise WebPlantViewFunctionRunError(self._driver_id, message, error)

    # # ------------------------------
    # def send_key(self, key: str):
    #     """
    #     [ 弹窗输入框键入文本 ]

    #     ---
    #     参数:
    #         key { str } : 文本.

    #     """
        
    #     try:
    #         message = Regular.get_function_doc_name(self.send_key.__doc__)
    #         self._handler.switch_to.alert.send_keys(key)
    #         execution_step_record(self._driver_id, message, key)

    #     except NoAlertPresentException:
    #         raise WebPlantViewFunctionRunError(self._driver_id, message, '当前没有弹窗')

    #     except BaseException as error:
    #         raise WebPlantViewFunctionRunError(self._driver_id, message, error)


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
class WebPlantViewFunctionRunError(Exception):
    """ [ Web视图函数执行异常 ] """
    
    def __init__(self, driver_id: int, message: str, error: Any):
        self.message = f'error :: { message } :: { error } !'
        self.err_name = Regular.get_function_doc_name(self.__doc__)
        execution_step_record(driver_id, message, level='error')

    def __str__(self) -> str:
        return ''.join([self.err_name, ' :: ', self.message])
