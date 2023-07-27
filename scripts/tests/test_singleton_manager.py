import pytest
from scripts.program.singleton_manager import Manager
import os 
import json 
import shutil 
import scripts.program.scripts_constants as CONSTANTS

@pytest.fixture
def test_path():
    return os.getcwd()

@pytest.fixture
def manager(test_path):
    return Manager(test_path)

@pytest.fixture
def clear(manager):
    return shutil.rmtree(manager.get_data_path())

def test_singleton(test_path):
    """
    Manager should be initialized only once
    """
    manager1 = Manager(test_path)
    manager2 = Manager(test_path)
    assert manager1 is manager2
    
def test_get_root_path(test_path, manager):
    assert manager.get_root_path() == test_path

def test_set_up(manager):
    if os.path.exists(manager.get_data_path()):
        shutil.rmtree(manager.get_data_path())
    flag = manager.setup_data()
    assert os.path.exists(manager.get_data_path()) == True
    assert flag == True
    flag = manager.setup_data()
    assert flag == False
    with open(os.path.join(manager.get_data_path(), "data.json"), "r") as fp:
        data = json.load(fp)
        assert data[CONSTANTS.PROJECT_NUM] == 0
        assert len(data[CONSTANTS.PROJECTS]) == 0

    shutil.rmtree(manager.get_data_path())

def test_create_project(manager):
    project_id = "demo1-yzhuang63@wisc.edu-07:20:2023-14:28:59"
    project_path = os.path.join(manager.get_data_path(), project_id)
    manager.create_project(project_id)
    with open(os.path.join(project_path, project_id + ".json"), "r") as fp:
        data = json.load(fp)
        assert data[CONSTANTS.TASK_NUM] == 0
        assert len(data[CONSTANTS.TASKS]) == 0
    with open(os.path.join(manager.get_data_path(), "data.json"), "r") as fp:
        data = json.load(fp)
        assert data[CONSTANTS.PROJECT_NUM] == 1
        assert len(data[CONSTANTS.PROJECTS]) == 1
        assert data[CONSTANTS.PROJECTS][project_id] == os.path.join(manager.get_data_path(), project_id)
    shutil.rmtree(manager.get_data_path())
