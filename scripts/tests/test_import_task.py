import pytest
import json
import sys
import os
import scripts.program.scripts_constants as CONSTANTS
from scripts.program.task_import import TaskImport
from scripts.program.metadata.task_metadata import TaskOutputDescription

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
    result_path = os.path.join(task_folder, CONSTANTS.RESULT_JSON)
    assert os.path.exists(result_path)
    imagesets_path = os.path.join(task_folder, CONSTANTS.IMAGESET_JSON)
    assert os.path.exists(imagesets_path)

    # 4. test will deserialize result.json to find result file of imageset.json
    loaded_task = TaskOutputDescription.load_from_json(result_path)
    # TODO: verify the imagesets path in the results.
    # TODO: verify the gain file is findable.

    # 5. test will deserialize imageset.json, verify the correct filenames are listed.
    # ImageSet()

