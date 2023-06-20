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

from task_import import Task_Import

def test_import_from_frames():
    """
    Test we can correctly import from a 'frames' folder.
    """

