"""
This module is used for the interface of All kinds of Task class
"""
import os
from abc import ABC, abstractmethod, abstractproperty
from typing import List

import scripts_constants
from metadata.task_metadata import TaskDescription, TaskOutputDescription

class Task(ABC):
    """
        This class acts as an interface, defining the common methods and access expected for
        any job/task of a processing pipeline.  This class is expected to be the representation
        for the backend describing how to start/run a process.  It is also expected to be an
        interface queried by the UI to be able to show what a task is, and how it was run.
    """

    # This should be constant for all tasks
    task_json = scripts_constants.TASK_JSON
    result_json = scripts_constants.RESULT_JSON
    imageset_filename = scripts_constants.IMAGESET_JSON
    task_folder = ''
    parameters = {}

    def get_result(self):
        """
        this method should get the result of the completing task
        """
        result_path= os.path.join(self.task_folder, self.result_json)
        loaded_task = TaskOutputDescription.load_from_json(result_path)
        return loaded_task

    def get_parameter(self, key: str) -> str:
        """
        Return the value of a parameter for the task
        :param key: name of a name:value pair to get a parameter
        :return: the parameter value for the key 
        """
        return self.parameters[key]
    
    def set_parameter(self, key:str, value:str):
        """
        Set a value of a parameter for the task
        :param key: name of a name:value pair to get a parameter
        :param value: the value to assign.
        """
        self.parameters[key] = value

    @abstractmethod
    def name(self) -> str:
        """
        This method should return the name for this task
        :return: string
        """

    @abstractmethod
    def description(self) -> str:
        """
        This method should return the detailed description of the task
        :return: string
        """

    @abstractmethod
    def run(self):
        """
        this method should actually run the task; must be implemented by each task.
        appropriate metadata should be serialized by the task.
        """