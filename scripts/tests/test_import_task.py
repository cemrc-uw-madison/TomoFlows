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

import scripts_constants
from task_import import TaskImport

from metadata.task_metadata import TaskOutputDescription

def test_import_from_frames(tmp_path):
    """
    Test we can correctly import from a 'frames' folder.
    """

    # 1. in a temporary directory, create mock files
    mock_frames_path = os.path.join(tmp_path, 'frames')
    mock_frames_example_path = os.path.join(mock_frames_path, 'grid_0005')
    os.makedirs(mock_frames_example_path)
    
    # 2. task import will import that folder filenames
    task_folder = os.path.join(tmp_path, 'task_import_01')
    os.makedirs(task_folder)
    task = TaskImport(task_folder)
    task.parameters['import_data'] = mock_frames_path
    task.parameters['import_directory_type'] = 'frames'
    task.run()

    # 3. task import will serialize the imageset.json and result.json
    result_path = os.path.join(task_folder, scripts_constants.RESULT_JSON)
    assert os.path.exists(result_path)
    imagesets_path = os.path.join(task_folder, scripts_constants.IMAGESET_JSON)
    assert os.path.exists(imagesets_path)

    # 4. test will deserialize result.json to find result file of imageset.json
    loaded_task = TaskOutputDescription.load_from_json(result_path)
    # TODO: verify the imagesets path in the results.
    # TODO: verify the gain file is findable.

    # 5. test will deserialize imageset.json, verify the correct filenames are listed.
    # ImageSet()
