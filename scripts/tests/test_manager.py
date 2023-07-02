import pytest
from program import manager 
import os 
import json 
import shutil 
from program.scripts_constants import TASK_NUM, PROJECT_ID, TASKS, PROJECT_NUM, PROJECTS
test_path = os.getcwd()
os.chdir("../..")
root_path = os.getcwd()
def test_get_root_path1():
    """
    Test if get_root_path can return correct root path from any directory
    """
    os.chdir(os.getcwd() + "/scripts/tests")
    assert manager.get_root_path() == root_path

def test_get_root_path2():
    """
    Test if get_root_path can return correct root path from any directory
    """
    os.chdir("../..")
    os.chdir(os.getcwd() + "/server")
    assert manager.get_root_path() == root_path

def test_get_root_path3():
    """
    Test if get_root_path return -1 if current working directory not inside /TomoFlows
    """
    os.chdir("../..")
    assert manager.get_root_path() == -1

def test_create_data_folder1():
    os.chdir(test_path)
    flag = manager.create_data_folder(test_path)
    assert os.path.exists(os.path.join(test_path, "data")) == True
    assert flag == True

def test_create_data_folder2():
    flag = manager.create_data_folder(test_path)
    assert flag == False
    os.rmdir(os.path.join(test_path, "data"))

def test_create_data_metadata1():
    """
    Test if create_data_metadata create json file correctly
    """
    if manager.create_data_folder(test_path):
        data_path = os.path.join(test_path, "data")
        assert manager.create_data_metadata(data_path) == True
        json_path = os.path.join(data_path, "data.json")
        with open(json_path, "r") as fp:
            data = json.load(fp)
            assert data[PROJECT_NUM] == 0
            assert len(data[PROJECTS]) == 0

def test_create_data_metadata2():
    """
    Test if create_data_metadata return False if data.json exists already
    """
    data_path = os.path.join(test_path, "data")
    assert manager.create_data_metadata(data_path) == False 
    shutil.rmtree(data_path)

def test_create_project_folder1():
    manager.create_data_folder(test_path)
    data_path = os.path.join(test_path, "data")
    assert manager.create_project_folder(data_path, 1) == True 
    assert "project_1" in os.listdir(data_path)

def test_create_project_folder2():
    data_path = os.path.join(test_path, "data")
    assert manager.create_project_folder(data_path, 1) == False 
    assert "project_1" in os.listdir(data_path)
    assert manager.create_project_folder(data_path, 2) == True 
    assert "project_2" in os.listdir(data_path)
    shutil.rmtree(data_path)

def test_create_project():
    manager.setup_data(test_path)
    data_path = os.path.join(test_path, "data")
    for _ in range(5):
        manager.create_project(data_path)
    with open(os.path.join(data_path, "data.json"), "r") as fp:
        data_json = json.load(fp)
        assert data_json[PROJECT_NUM] == 5
        assert len(data_json[PROJECTS]) == 5
        for i in range(5):
            project_name = "project_" + str(i + 1)
            assert data_json[PROJECTS][project_name] == os.path.join(data_path, project_name)
    shutil.rmtree(data_path)
    

    