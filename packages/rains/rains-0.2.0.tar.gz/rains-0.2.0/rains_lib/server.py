import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.core.perform_server import PerformServer
perform_server = PerformServer()
perform_server.running()
