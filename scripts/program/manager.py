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
import scripts.program.scripts_constants as CONSTANTS


def get_root_path():
    """
    get_root_path should be able to get /TomoFlow path from anywhere inside /TomoFlow, like /TomoFlow/scripts
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
    os.mkdir(data_path)
    return True
    
def create_data_metadata(path):
    """
    create_data_metadata should be able to create metadata for all projects
    what infomation should be stored in metadata needs discussion
    Arguments: 
    1. path: absolute path of /data
    return True if data.json is successfully created
    return False if data.json exists 
    """
    if "data.json" in os.listdir(path):
        return False
    info = {CONSTANTS.PROJECT_NUM: 0, CONSTANTS.PROJECTS: {}}
    json_info = json.dumps(info)
    json_path = os.path.join(path, "data.json")
    with open(json_path, "w") as fp:
        fp.write(json_info)
    return True

def setup_data(path):
    """
    setup_data is a wrapper of create_data_folder and create_data_metadata
    Arguments:
    path: absolute path to create /data
    return False if setup fails
    return True if setup succeeds
    """
    if not create_data_folder(path):
        return False
    data_path = os.path.join(path, "data")
    if not create_data_metadata(data_path):
        return False 
    return True

def create_project_folder(path, project_id):
    """
    create_project_folder needs the project's information to generate a unique folder
    what information is required needs discussion
    Arguments: 
    1. path: absolute path of /data
    2. project_id: project's id 
    return True if /project_id is successfully created
    return False if /project_id exists
    """
    project_name = "project_" + str(project_id)
    if project_name in os.listdir(path):
        return False 
    project_path = os.path.join(path, project_name)
    os.mkdir(project_path)
    return True

def create_project_metadata(path, project_id):
    """
    create_project_metadata should be able to create project metadata based on given arguments
    what infomation should be stored in metadata needs discussion
    Arguments: 
    1. path: absolute path of /data
    2. project_id: project's id 
    return True if project_id.json is successfully created
    return False if project_id.json exists or project_id doesn't exists in data.json
    """
    project_name = "project_" + str(project_id)
    if "data.json" not in os.listdir(path) or project_name not in os.listdir(path):
        return False
    project_path = os.path.join(path, project_name)
    project_json = project_name + ".json"
    if project_json in os.listdir(project_path):
        return False
    json_path = os.path.join(project_path, project_json)
    with open(json_path, "w") as fp:
        info = {CONSTANTS.TASK_NUM: 0, CONSTANTS.TASKS: {}, CONSTANTS.PROJECT_ID: project_id}  
        fp.write(json.dumps(info))
    return True    

def create_project(data_path):
    """
    create_project is a wrapper of create_project_folder and create_project_metadata
    Arguments:
    data_path: absolute path to create project on
    It should return False if project creation fails and return True if project is successfully created  
    """

    data_json_path = os.path.join(data_path, "data.json")
    with open(data_json_path, "r+") as fp:
        data_json = json.load(fp)
        project_id = data_json[CONSTANTS.PROJECT_NUM] + 1
        if not create_project_folder(data_path, project_id):
            return False
        if not create_project_metadata(data_path, project_id):
            return False 
        data_json[CONSTANTS.PROJECT_NUM] = project_id
        project_name = "project_" + str(project_id)
        data_json[CONSTANTS.PROJECTS][project_name] = os.path.join(data_path, project_name)
        fp.seek(0)
        json.dump(data_json, fp)
    return True
    

def create_task_folder(path):
    """
    create_task_folder needs the task's information to generate a unique folder
    what information is required needs discussion
    """
    pass



def create_task_metadata(path):
    """
    create_task_metadata should be able to create task metadata based on given arguments
    what infomation should be stored in metadata needs discussion
    """
    pass

def update_data_metadata(path, info):
    """
    update_data_metadata should be able to update the latest information of tasks or projects on server
    Arguments:
    path: absolute path where /data located
    info: information needs to be updated
    """
    pass 

