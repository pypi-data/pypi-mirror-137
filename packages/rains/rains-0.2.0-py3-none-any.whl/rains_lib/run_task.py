import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import shutil
import pathlib
import importlib
from pathlib import Path

from rains.core.perform_pool import PerFormPool


def analysis_py_file_tasks(imp_analysis_str: str) -> list:
    tasks = []

    module = importlib.import_module(imp_analysis_str)
    for n in module.__dict__.keys():
        if 'Task' in n[0:4]:
            tasks.append(module.__dict__[n])

    return tasks

task_list = []
if len(sys.argv) >= 2:

    for i in sys.argv[1:]:

        root_task_path: Path = Path(sys.argv[0]).parent.joinpath('task_cache')
        path = Path(i)

        # 参数是目录
        if path.is_dir():
            imp_analysis_str = 'task_cache'
            dir_parent_name = pathlib.WindowsPath(str(i)).parts[-1]
            save_dir = root_task_path.joinpath(dir_parent_name)
            save_dir.mkdir(parents=True, exist_ok=True)
            imp_analysis_str += f'.{ dir_parent_name }'

            py_list = path.glob('task*.py')
            for i in py_list:
                cache_task = save_dir.joinpath(i.name)
                cache_task.write_bytes(i.read_bytes())
                task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ i.stem }')

        # 参数是文件
        else:
            if path.suffix != '.py':
                path = Path(f'{ str(path) }.py')
            imp_analysis_str = 'task_cache'
            dir_parent_name = pathlib.WindowsPath(str(i)).parts[-2]
            save_dir = root_task_path.joinpath(dir_parent_name)
            save_dir.mkdir(parents=True, exist_ok=True)
            imp_analysis_str += f'.{ dir_parent_name }'
            cache_task = save_dir.joinpath(path.name)
            cache_task.write_bytes(path.read_bytes())
            task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ path.stem }')


perform_pool = PerFormPool()
for task in task_list:
    perform_pool.put_task(task)
    
perform_pool.running()
shutil.rmtree(root_task_path)
