import os
import json
import scripts.program.scripts_constants as CONSTANTS

class Manager:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, path):
        # path represents BASE_DIR in django, the directory where manager.py is located
        
        self.path = path
        self.data_path = os.path.join(path, CONSTANTS.DATA_SUBFOLDER)
        self.setup_data()

    def get_root_path(self):
        """
        get_root_path should be able to get /TomoFlow path from anywhere inside /TomoFlow, like /TomoFlow/scripts
        """
        return self.path
    
    def get_data_path(self):
        return self.data_path
    
    def create_data_folder(self):
        """
        create_data_folder will create /data folder on given path
        """
        
        if os.path.exists(self.data_path):
            # if /data exists, there is no need to call create_data folder
            return False
        os.mkdir(self.data_path)
        return True
        
    def create_data_metadata(self):
        """
        create_data_metadata should be able to create metadata for all projects
        what infomation should be stored in metadata needs discussion
        Arguments: 
        return True if data.json is successfully created
        return False if data.json exists 
        """
        
        if "data.json" in os.listdir(self.data_path):
            return False
        info = {CONSTANTS.PROJECT_NUM: 0, CONSTANTS.PROJECTS: {}}
        json_info = json.dumps(info)
        json_path = os.path.join(self.data_path, "data.json")
        with open(json_path, "w") as fp:
            fp.write(json_info)
        return True

    def setup_data(self):
        """
        setup_data is a wrapper of create_data_folder and create_data_metadata
        Arguments:
        return False if setup fails
        return True if setup succeeds
        """
        if not self.create_data_folder() or not self.create_data_metadata():
            return False
        return True

    def create_project_folder(self, project_id):
        """
        create_project_folder needs the project's information to generate a unique folder
        what information is required needs discussion
        Arguments: 
        1. path: absolute path of /data
        2. project_id: project's identifier, using format project_name-owner's email-first created time
        return True if /project_id is successfully created
        return False if /project_id exists
        """
        
        if project_id in os.listdir(self.data_path):
            return False 
        project_path = os.path.join(self.data_path, project_id)
        os.mkdir(project_path)
        return True

    def create_project_metadata(self, project_id):
        """
        create_project_metadata should be able to create project metadata based on given arguments
        what infomation should be stored in metadata needs discussion
        Arguments: 
        1. path: absolute path of /data
        2. project_id: project's identifier, using format project_name-owner's email-first created time 
        return True if project_id.json is successfully created
        return False if project_id.json exists or project_id doesn't exists in data.json
        """
        
        if "data.json" not in os.listdir(self.data_path) or project_id not in os.listdir(self.data_path):
            return False
        project_name = project_id.split("-")[0]
        owner = project_id.split("-")[1]
        created_at = project_id.split("-")[2]
        project_path = os.path.join(self.data_path, project_id)
        project_json = project_id + ".json"
        if project_json in os.listdir(project_path):
            return False
        json_path = os.path.join(project_path, project_json)
        with open(json_path, "w") as fp:
            info = {CONSTANTS.TASK_NUM: 0, CONSTANTS.TASKS: {},
                    CONSTANTS.PROJECT_ID: project_id, CONSTANTS.PROJECT_NAME: project_name, CONSTANTS.OWNER: owner, CONSTANTS.CREATED_AT: created_at}  
            fp.write(json.dumps(info))
        return True    

    def create_project(self, project_id):
        """
        create_project is a wrapper of create_project_folder and create_project_metadata
        Arguments:
        data_path: absolute path to create project on
        It should return False if project creation fails and return True if project is successfully created  
        """

        data_json_path = os.path.join(self.data_path, "data.json")
        with open(data_json_path, "r+") as fp:
            data_json = json.load(fp)
            if not self.create_project_folder(project_id):
                return False
            if not self.create_project_metadata(project_id):
                return False 
            data_json[CONSTANTS.PROJECT_NUM] = data_json[CONSTANTS.PROJECT_NUM] + 1
            data_json[CONSTANTS.PROJECTS][project_id] = os.path.join(self.data_path, project_id)
            fp.seek(0)
            json.dump(data_json, fp)
        return True
        

    def create_task_folder(path):
        """
        create_task_folder needs the task's information to generate a unique folder
        what information is required needs discussion
        """
        pass


    def list_task(path, project_id):
        """
        List all associated tasks for specific project
        path: absolute path where /data located
        project_id: integer, id of project
        return: False if project doesn't exist, List of task's name is project exists
        """
        data_json_path = os.path.join(path, "data.json")
        project_name = "project_" + str(project_id)
        with open(data_json_path, "r+") as fp:
            data_json = json.load(fp)
            if project_name not in data_json[CONSTANTS.PROJECTS]:
                return False
            project_json = os.path.join(data_json[CONSTANTS.PROJECTS][project_name], "project.json")
            with open(project_json, "r") as project_fp:
                project_json = json.load(project_fp)
                return project_json[CONSTANTS.TASKS].keys()

        
    def create_task_metadata(self):
        """
        create_task_metadata should be able to create task metadata based on given arguments
        what infomation should be stored in metadata needs discussion
        """
        pass

    def update_data_metadata(self):
        """
        update_data_metadata should be able to update the latest information of tasks or projects on server
        Arguments:
        path: absolute path where /data located
        info: information needs to be updated
        """
        pass 

