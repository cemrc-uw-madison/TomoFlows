import pytest
from program import manager 
import os 

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