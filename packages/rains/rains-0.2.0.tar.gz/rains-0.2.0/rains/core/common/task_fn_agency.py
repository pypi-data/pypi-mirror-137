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
[ Rains.Common.Task.TaskFnAgency ]

"""

import inspect
from typing import Any

from rains.baseic.keyword import KEYWORD


# ----------------------------------
class TaskFnAgency(object):
    """
    [ 函数代理 ]

    * 该类主要职责于执行 JSON 译文串.

    * 通过传递模块名、类名、方法名、元素定位、传递参数的方式调用目标函数.

    """

    _kit_plant: Any = None
    """ [ 测试套件工厂构建类 ] """

    _module_living = None
    """ [ 模块类实例 ] """

    _class_living = None
    """ [ 执行类实例 ] """

    _translation_dict: dict
    """ [ JSON 译文串容器 ] """

    # ------------------------------
    def __init__(self, kit_plant: Any):
        """
        [ 函数代理 ]
        
        ---
        参数:
            kit_plant { Any } : 测试套件工厂构建类.

        """

        self._kit_plant = kit_plant

    # ------------------------------
    def map(self, translation_dict: dict):
        """
        [ 映射函数 ]

        * 通过传递类名、方法名、参数字典的形式调用指定函数.
        
        ---
        参数:
            translation_dict { dict } : JSON 串.

        """

        self._translation_dict = translation_dict
        self._analysis_map_living()
        self._analysis_run_living()
        return self._running_function()

    # ------------------------------
    def _analysis_map_living(self):
        """
        [ 解析映射类实例 ]

        """

        try:
            module = self._translation_dict[KEYWORD.TASK.JSON_ARG_MODULE]

            legal_modules = [m for m in type(self._kit_plant).__dict__.keys() if '_' not in m]
            if module not in legal_modules:
                err_mgs = f"异常 :: 模块不存在 :: '{ module }' not in { legal_modules } !"
                raise Exception(err_mgs)

            if module == 'element':

                if KEYWORD.TASK.JSON_ARG_ELEMENT not in self._translation_dict.keys():
                    err_mgs = f"缺少元素定位描述 :: 参数必须携带 [{ KEYWORD.TASK.JSON_ARG_ELEMENT }] !"
                    raise Exception(err_mgs)

                element: dict = self._translation_dict[KEYWORD.TASK.JSON_ARG_ELEMENT]
                element.update({'self': self._kit_plant})

                parameters = []
                sign = inspect.signature(self._kit_plant.element)
                for k, v in sign.parameters.items():
                    if v.default == inspect._empty:
                        if k not in element.keys():
                            raise Exception(f'元素定位描述缺少参数 :: [{ k }]')
                    value = v.default if k not in element.keys() else element[k]
                    parameters.append(value)

                self._map_living = self._kit_plant.element(*parameters)
            
            else:
                self._map_living = type(self._kit_plant).__dict__[f'_map_{ module }'](self._kit_plant)

        except BaseException as err:
            raise Exception(str(err))

    # ------------------------------
    def _analysis_run_living(self):
        """
        [ 解析执行类实例 ]

        """

        try:
            run_class = self._translation_dict[KEYWORD.TASK.JSON_ARG_CLASS]
            unstrained_class_dict = type(self._map_living).__dict__

            if run_class not in unstrained_class_dict:
                raise Exception(f'{ type(self._map_living) } there is no such map :: { run_class }')

            self._run_living = unstrained_class_dict[f'_map_{ run_class }'](self._map_living)
    
        except BaseException as err:
            raise Exception(str(err))

    # ------------------------------
    def _running_function(self):
        """
        [ 执行函数 ]

        """

        try:
            function = self._translation_dict[KEYWORD.TASK.JSON_ARG_FUNCTION]
            unstrained_class_dict = type(self._run_living).__dict__

            if function not in unstrained_class_dict:
                raise Exception(f'{ type(self._run_living) } there is no such function :: { function }')

            function_living = type(self._run_living).__dict__[function]

            parameter: dict = {}
            if KEYWORD.TASK.JSON_ARG_PARAMETER in self._translation_dict.keys():
                parameter = self._translation_dict[KEYWORD.TASK.JSON_ARG_PARAMETER]
            parameter.update({'self': self._run_living})

            parameters = []
            sign = inspect.signature(function_living)
            for k, v in sign.parameters.items():
                if v.default == inspect._empty:
                    if k not in parameter.keys():
                        raise Exception(f'{ function } missing para :: { k }')
                value = v.default if k not in parameter.keys() else parameter[k]
                parameters.append(value)

            return function_living(*parameters)
            
        except BaseException as err:
            raise Exception(str(err))
