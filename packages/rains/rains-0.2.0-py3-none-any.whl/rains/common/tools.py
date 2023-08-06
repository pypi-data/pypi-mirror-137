import os
import sys


def add_execute_depend_path():
    """
    [ 增加执行依赖路径 ]

    * NOT MESSAGE

    """

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
