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
[ Rains.Kit.Api.ApiPlant ]

"""

from typing import Any

from rains.kit.api.packaging.api_plant_handler import ApiPlantHandler
from rains.kit.api.packaging.api_plant_request import ApiPlantRequest


# ----------------------------------
class ApiPlant(object):
    """
    [ Api 工厂构建类 ]

    """
    
    _api_driver: Any
    """ [ Api 驱动程序 ] """
    
    # ------------------------------
    def __init__(self, api_driver: Any):
        """
        [ Api 工厂构建类 ]

        ---
        参数:
            web_driver { WebDriver } : Web 驱动程序.

        """

        self._api_driver = api_driver
        
    # ------------------------------
    @property
    def driver(self):
        return self._api_driver

    # ------------------------------
    @property
    def handler(self):
        return ApiPlantHandler(self._api_driver)

    # ------------------------------
    def _map_handler(self):
        return self.handler

    # ------------------------------
    @property
    def request(self):
        return ApiPlantRequest(self._api_driver)

    # ------------------------------
    def _map_request(self):
        return self.request
