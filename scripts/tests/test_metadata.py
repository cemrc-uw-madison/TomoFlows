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
absolute_list[-1] = "metadata/"
sys.path.append("/".join(absolute_list))

from metadata import TaskDescription

@pytest.fixture
def sample_task():
    task = TaskDescription('Task_Gain', 'Image format conversion task')
    task.add_parameter('param_input_tiff', 'Gain.tiff')
    task.add_parameter('param_output_mrc', 'Gain.mrc')
    return task

def test_save_and_load_json(sample_task, tmp_path):
    # Save task to JSON
    filename = tmp_path / 'task_description.json'
    sample_task.save_to_json(str(filename))

    # Load task from JSON
    loaded_task = TaskDescription.load_from_json(str(filename))

    # Check task attributes
    assert loaded_task.task_name == sample_task.task_name
    assert loaded_task.task_description == sample_task.task_description
    assert loaded_task.parameters == sample_task.parameters

def test_save_and_load_json_file_content(sample_task, tmp_path):
    # Save task to JSON
    filename = tmp_path / 'task_description.json'
    sample_task.save_to_json(str(filename))

    # Load JSON file and compare its content
    with open(filename, 'r') as file:
        loaded_data = json.load(file)

    assert loaded_data['task_name'] == sample_task.task_name
    assert loaded_data['task_description'] == sample_task.task_description
    assert loaded_data['parameters'] == sample_task.parameters
