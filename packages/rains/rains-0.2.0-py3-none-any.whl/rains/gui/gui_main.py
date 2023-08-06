
import os
import yaml
import pathlib
import PySimpleGUI as Sg

from PySimpleGUI import Window

from rains.baseic.consts import ConstPath
from rains.baseic.decorator import singleton_pattern

from rains.gui.page.pg_create_project import pg_create_project_show


@singleton_pattern
class GuiMain(object):
    """

    """

    _main_window: Window
    _data_path: pathlib.Path
    _data_dict: list

    def __init__(self):
        self._main_window = pg_create_project_show()

        # 如果不存在 GuiData.yaml 文件，则创建
        self._data_path = pathlib.Path(os.path.abspath(__file__)).parent.joinpath('GuiData.yaml')

        if not self._data_path.is_file():
            self._data_path.touch(mode=0o777)

            with open(str(self._data_path.resolve()), 'w', encoding='UTF-8') as f:
                base_data = {
                    'SIGN_PROJECT_LIST': {
                        'A': {
                            'name': 'A',
                            'path': 'c/a'
                        },
                        'B': {
                            'name': 'B',
                            'path': 'c/b'
                        }
                    }
                }
                yaml.dump(base_data, f, allow_unicode=True)

        data_yaml = open(str(self._data_path.resolve()), encoding='UTF-8')
        self._data_dict = yaml.load(data_yaml, Loader=yaml.FullLoader)

        print(self._data_path)
        print(self._data_dict)

    def running(self):
        """

        """

        while True:

            event, values = self._main_window.read()

            # 事件::主窗口关闭
            if event == Sg.WIN_CLOSED:
                print('页面关闭')
                break

            # 事件::创建项目
            if event == '创建项目':
                self.create_project(values)

            print(f'{event}')
            print(f'{values}')

            self._main_window.close()

    def create_project(self, values):
        """

        """

        if not values[0]:
            print('没有选择文件夹')

            if not values[1]:
                print('没有输入项目名称')

        else:
            create_project_path = f'{values[0]}/{values[1]}'
            print(create_project_path)
