
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.kit.web import *
from rains.kit.api import ApiTask


class ApiTest(ApiTask):
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


class TASK:
    def __init__(self) -> None:
        print("123456")


class TaskTest(WebTask):
    """
    测试任务
    """

    def set_task_init(self):
        
        print('set_task_init')

        self.user_input = self.plant.element(
            page='超管后台', 
            name='邮箱输入框', 
            by_key=BY.XPATH, 
            by_value='/html/body/div/div/div/div/div[2]/form/div[1]/div/input'
        )

        self.password_input = self.plant.element(
            page='超管后台', 
            name='密码输入框', 
            by_key=BY.XPATH, 
            by_value='/html/body/div/div/div/div/div[2]/form/div[2]/div/input'
        )

        self.login_button = self.plant.element(
            page='超管后台', 
            name='Login按钮', 
            by_key=BY.XPATH, 
            by_value='/html/body/div/div/div/div/div[2]/form/div[4]/div/button'
        )

        self.create_button = self.plant.element(
            page='超管后台', 
            name='Login按钮', 
            by_key=BY.XPATH, 
            by_value='/html/body/div/div/div/div/div/div[1]/a'
        )

    def set_task_quit(self):
        self.plant.view.get.url()
        print('set_task_quit')

    def set_case_init(self):
        print('set_case_init')
        self.plant.view.page.goto('http://manage.dev-tea.cblink.net/')

    def set_case_quit(self):
        print('set_case_quit')

    def case_1(self):
        """
        登录成功
        """
        self.plant.view.get.url()
        self.user_input.input.send('admin@baocai.us')
        self.password_input.input.send('123456')
        self.login_button.mouse.tap()
        return self.create_button.get.exist() is True

    def case_2(self):
        """
        登录成功
        """
        return self.create_button.get.exist() is True


task_dict = {
    'task_name': 'TestJsonTask', 
    'task_type': 'WEB',
    'task_remark': '测试JSON任务', 
    'instructions_setter': {}, 
    'instructions_case': {
        'case_1': {
            'case_remark': '测试JSON用例1', 
            'assert': {5: True}, 
            'step_list': {
                1: {
                    'module': 'view', 
                    'class': 'page', 
                    'function': 'goto', 
                    'parameter': {
                        'url': 'http://manage.dev-tea.cblink.net/'
                    }
                }, 
                2: {
                    'module': 'element', 
                    'class': 'input', 
                    'function': 'send', 
                    'element': {
                        'page': '超管后台', 
                        'name': '邮箱输入框', 
                        'by_key': 'xpath', 
                        'by_value': '/html/body/div/div/div/div/div[2]/form/div[1]/div/input'
                    }, 
                    'parameter': {
                        'key': 'admin@baocai.us'
                    }
                }, 
                3: {
                    'module': 'element', 
                    'class': 'input', 
                    'function': 'send', 
                    'element': {
                        'page': '超管后台', 
                        'name': '密码输入框', 
                        'by_key': 'xpath', 
                        'by_value': '/html/body/div/div/div/div/div[2]/form/div[2]/div/input'
                    }, 
                    'parameter': {
                        'key': '123456'
                    }
                }, 
                4: {
                    'module': 'element', 
                    'class': 'mouse', 
                    'function': 'tap', 
                    'element': {
                        'page': '超管后台', 
                        'name': 'Login按钮', 
                        'by_key': 'xpath', 
                        'by_value': '/html/body/div/div/div/div/div[2]/form/div[4]/div/button'
                    }
                }, 
                5: {
                    'module': 'element', 
                    'class': 'get', 
                    'function': 'exist', 
                    'element': {
                        'page': '超管后台', 
                        'name': 'Login按钮', 
                        'by_key': 'xpath', 
                        'by_value': '/html/body/div/div/div/div/div/div[1]/a'
                    }
                }
            }
        }
    }
}


if __name__ == '__main__':
    # rains.core.rains_server import RainsServer
    # rains_server = RainsServer()
    # rains_server.running()

    # from rains.core.rains_pool import RainsPool
    # rains_pool = RainsPool(debug=True)

    # for _i in range(1):
    #     rains_pool.put_core(WebDriver())

    # for _i in range(1):
    #     rains_pool.put_task(TaskTest)
    #     rains_pool.put_task(task_dict)

    # rains_pool.running()

    # from rains.kit.web import WebDriver
    # core = WebDriver()
    # core.start_task(TaskTest)
    # core.end()

    from rains.core.perform_pool import PerFormPool
    from rains.kit.web import WebDriver

    # with WebDriver() as driver:
    #     driver.start_task(task_dict)
    #     # driver.start_task(task_dict)

    pool = PerFormPool()
    pool.put_task(task_dict)
    pool.put_task(TaskTest)
    pool.running()
