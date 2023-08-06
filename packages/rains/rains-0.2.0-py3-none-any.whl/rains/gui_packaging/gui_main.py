
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
    _gui_data: list

    def __init__(self):
        self._main_window = pg_create_project_show()

        data_yaml = open(ConstPath.ROOT.joinpath('gui/data.yaml'), encoding='UTF-8')
        self._gui_data = yaml.load(data_yaml, Loader=yaml.FullLoader)

        print(ConstPath.ROOT.joinpath('gui/data.yaml'))
        print(self._gui_data)

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
