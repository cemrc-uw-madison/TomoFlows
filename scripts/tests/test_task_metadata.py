import pytest
import json
import sys
import os
from scripts.program.metadata.task_metadata import TaskDescription
from scripts.program.metadata.task_metadata import TaskOutputDescription

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

@pytest.fixture
def sample_output_task():
    task = TaskOutputDescription('Task_Gain', 'Image format conversion task')
    task.add_output_file('job/Gain.tiff', 'tiff')
    task.add_log_file('tif2mrc.stdout')
    task.add_log_file('tif2mrc.stderr')
    task.set_status('Success')
    return task

def test_output_save_and_load_json(sample_output_task, tmp_path):
    filename = tmp_path / 'task_output_description.json'
    sample_output_task.save_to_json(str(filename))

    # Load task from JSON
    loaded_task = TaskOutputDescription.load_from_json(str(filename))

    # Check saved values
    assert loaded_task.task_name == sample_output_task.task_name
    assert loaded_task.task_description == sample_output_task.task_description
    assert loaded_task.output_files == sample_output_task.output_files
    assert loaded_task.logs == sample_output_task.logs
    assert loaded_task.status == sample_output_task.status

def test_output_save_and_load_json_file_content(sample_output_task, tmp_path):
    # Save task to JSON
    filename = tmp_path / 'task_output_description.json'
    sample_output_task.save_to_json(str(filename))

    # Load JSON file and compare its content
    with open(filename, 'r') as file:
        loaded_data = json.load(file)

    assert loaded_data['task_name'] == sample_output_task.task_name
    assert loaded_data['task_description'] == sample_output_task.task_description
    assert loaded_data['output_files'] == sample_output_task.output_files
    assert loaded_data['logs'] == sample_output_task.logs
    assert loaded_data['status'] == sample_output_task.status

