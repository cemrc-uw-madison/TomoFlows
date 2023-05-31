# -*- coding: utf-8 -*-
"""Manager module docstring

1. Manager module should be able to create folder to hold projects' metadata and associated tasks 
2. Manager module should be able to create folder to hold tasks' metadata and all related data file
3. Manager module should be able to create metadata file for projects and tasks
4. Manager module should be able to update metadata file when user create or delete project or task
5. Manager should reflect the data on disk to database, cause the data on database will gone when the docker container is shutdown
"""
import os
import json

def get_root_path():
    """
    get_root_path should be able to get /TomoFlow path from anywhere
    """
    current_wd = os.getcwd()
    index = 0
    if "TomoFlows" not in current_wd:
        return -1
    for folder in current_wd.split("/"):
        index += 1
        if folder == "TomoFlows":
            break
    return "/".join(current_wd.split("/")[0: index])

def create_data_folder(path):
    """
    create_data_folder will create /data folder on given path
    """
    data_path = os.path.join(path, "data")
    if os.path.exists(data_path):
        # if /data exists, there is no need to call create_data folder
        return False
    print(data_path)
    os.mkdir(data_path)
    return True
    
def create_project_folder(path):
    """
    create_project_folder needs the project's information to generate a unique folder
    what information is required needs discussion
    """
    pass

def create_task_folder(path):
    """
    create_task_folder needs the task's information to generate a unique folder
    what information is required needs discussion
    """
    pass

def create_project_metadata(info):
    """
    create_project_metadata should be able to create project metadata based on given arguments
    what infomation should be stored in metadata needs discussion
    """
    pass

def create_task_metadata(info):
    """
    create_task_metadata should be able to create task metadata based on given arguments
    what infomation should be stored in metadata needs discussion
    """
    pass

def update_metadata(path):
    """
    update_metadata should be able to update the latest information of tasks or projects on server
    """
