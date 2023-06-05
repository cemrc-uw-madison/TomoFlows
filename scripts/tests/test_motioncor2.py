import pytest
import json

import sys
import os

# NOTE: we need absolute imports to reach the program module, 
# and it may be clearer to instead import as:
#   `from program.task_motioncor2 import TaskMotionCor2`
# which would require that the top-level program folder is included in the PYTHONPATH environment variable.

absolute_path = os.path.dirname(__file__)
absolute_list = absolute_path.split("/")
absolute_list[-1] = "program/"
sys.path.append("/".join(absolute_list))

from task_motioncor2 import TaskMotionCor2

def test_run_motioncor2(sample_task, tmp_path):
    ''' TODO: should take a prefilled parameters for a task and run this '''