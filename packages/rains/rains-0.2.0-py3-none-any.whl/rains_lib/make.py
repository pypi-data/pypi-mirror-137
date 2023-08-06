import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from rains.baseic.environment.make import create_runtime_environment
from rains.baseic.environment.make import create_project_template

# 创建项目环境
create_runtime_environment()
create_project_template()
