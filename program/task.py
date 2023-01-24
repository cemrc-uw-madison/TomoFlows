"""
This module is used for the interface of All kinds of Task class
"""
from abc import ABC, abstractmethod, abstractproperty


class Param:
    """
        This describes a single parameter description of a Task type:
        [Note: we may not need all the below]

        1. Human-readable name of parameter
        2. Description of the parameter (sentence or longer)
        3. Type of parameter (int, float, string)
        4. Range of parameter (min, max)
        5. Is this a required or optional parameter?
    """

    pass


class TaskType:
    """
        Class that represents a particular kind of Task.
    """

    pass


class Task(ABC):
    """
        This class acts as an interface, defining the common methods and access expected for
        any job/task of a processing pipeline.  This class is expected to be the representation
        for the backend describing how to start/run a process.  It is also expected to be an
        interface queried by the UI to be able to show what a task is, and how it was run.

       Task needs to provide these common items:
            1. This should provide a method that describes what kind of Task it is.
                - Deriving classes would be required to provide basics of information:
                -  Human-readable descriptions or a naming might be needed.
                -  Internal representation or naming could be needed.
            2. Methods to get a list of parameters (Param) for the Task.
            3. Methods to get/set a value for a particular Param.
            4. Method to actually execute the command.
                Expectation - initially this could just be a 'subprocess.call' direct execution
                This could also mean to give information required to run our task in a
                cluster computing system like SLURM or HTCondor.
            5. Method to get a list of results
            6. Method to get an output logs

        Task *could* provide these items:

            6. Methods to get actual command-line path of your command to execute
                (absolute path to reach the executable if needed)
                NOTE: we may not want #4, or there could be cases where this doesn't make sense.
            7. Method to clone and create a new runnable Task
            8. Methods to rerun, restart, or continue an interrupted Task.
                When/how could this work?  We may have a task that runs on 1000 images.
                It could be that 335 of the images processed, then the task was interrupted.
                If it is possible to restart the batch processing for the remaining images...
                then it could be possible to 'continue'.
    """

    @property
    @abstractproperty
    def param(self):
        """
        This method should return Parameter that needed to run the task
        :return: instance of Param class
        """

    @abstractmethod
    def description(self) -> str:
        """
        This method should return the detailed description of the task
        :return: string
        """

    @abstractmethod
    def get_param(self, key: str) -> [int, str]:
        """

        :param key: the parameter you want to get
        :return: the parameter value related to the key
        """

    @abstractmethod
    def run(self):
        """
        this method should actually run the task
        """

    @abstractmethod
    def get_result(self):
        """
        this method should get the result of the completing task
        """

    @abstractmethod
    def get_logs(self):
        """
        this method should get the logs created with the result
        """
