
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.kit.api.api_task import ApiTask
from rains.kit.api.api_driver import ApiDriver


class T(ApiTask):
    
    def case_01(self):
        r = self.plant.get('http://127.0.0.1:5000/get1')
        return r.data['code'] == 0
    
    def case_02(self):
        r = self.plant.get('http://127.0.0.1:5000/get1')
        return r.data['code'] == 0


api_driver = ApiDriver()
api_driver.start_task(T)
