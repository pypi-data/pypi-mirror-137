
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.kit.api import *
from rains.core.rains_pool import RainsPool


class TaskTest(ApiTask):
    """
    测试任务
    """

    url: str = 'http://127.0.0.1:5000'


    def case_01(self):
        """
        [ GET1 ]

        """

        r = self.plant.get(f'{ self.url }/get1')
        return r.data['code'] == 0 and r.data['data'] == 'get1'


    def case_02(self):
        """
        [ GET2 ]

        """

        r = self.plant.get(f'{ self.url }/get2')
        return r.data['code'] == 0 and r.data['data'] == 'get2'


    def case_03(self):
        """
        [ POST1 ]

        """

        data = {'v1': 1, 'v2': 2}
        r = self.plant.post(f'{ self.url }/post1', data)
        return r.data['code'] == 0 and r.data['data']['v2'] == '2'


    def case_04(self):
        """
        [ POST2 ]

        """

        data = {'v1': 1, 'v2': 2}
        self.plant.set_token('123123')
        r = self.plant.post(f'{ self.url }/post2', data)
        return r.data['data']['v2'] == '2' and r.data['token'] == '123123'


pool = RainsPool()
pool.put_core(ApiDriver())
pool.put_core(ApiDriver())
pool.put_task(TaskTest)
pool.put_task(TaskTest)
pool.put_task(TaskTest)
pool.running()
