import pytest
import json

import sys
import os

# NOTE: we need absolute imports to reach the metadata module, 
# and it may be clearer to instead import as:
#   `from program.metadata.metadata import TaskDescription``
# which would require that the top-level program folder is included in the PYTHONPATH environment variable.

absolute_path = os.path.dirname(__file__)
absolute_list = absolute_path.split("/")
absolute_list[-1] = "program/"
sys.path.append("/".join(absolute_list))

import scripts_constants
from metadata.workflow_metadata import WorkflowMetadata

@pytest.fixture
def sample_metadata():
    metadata = WorkflowMetadata()

    task1_params = {
        "import_data": 'example_folder_path/',
        "import_directory_type": "frames"
    }

    task2_params = {
        "param1": 5,
        "param2": "def"
    }

    metadata.add_task("Task1", task1_params)
    metadata.add_task("Task2", task2_params)

    return metadata

def test_save_and_load_json(sample_metadata, tmp_path):
    # Save metadata to JSON
    filename = tmp_path / scripts_constants.WORKFLOW_JSON
    sample_metadata.save_to_json(str(filename))

    # Load metadata from JSON
    loaded_metadata = WorkflowMetadata.load_from_json(str(filename))

    # Check number of tasks
    assert len(loaded_metadata.tasks) == len(sample_metadata.tasks)

    # Check task names and parameters
    for loaded_task, sample_task in zip(loaded_metadata.tasks, sample_metadata.tasks):
        assert loaded_task["name"] == sample_task["name"]
        assert loaded_task["parameters"] == sample_task["parameters"]

def test_save_and_load_json_file_content(sample_metadata, tmp_path):
    # Save metadata to JSON
    filename = tmp_path / scripts_constants.WORKFLOW_JSON
    sample_metadata.save_to_json(str(filename))

    # Load JSON file and compare its content
    with open(filename, "r") as file:
        loaded_data = json.load(file)

    assert loaded_data["tasks"] == sample_metadata.tasks