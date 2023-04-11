import typing
import subprocess
import os
from program.task import Task


def check_image_format(file_name, required_format):
    """

    :param file_name: provided file name
    :param required_format: required file format
    :return: if file has required format(Boolean value)
    """
    image_format = file_name.split(".")[-1]
    return image_format == required_format


class TaskStackAlignFrames(Task):
    """
    Run `alignframes` to assemble a stack
    """

    required_input_format = "mrc"
    required_output_format = "mrc"

    def __init__(self, input_file):
        """
        :param input_file: file name in format conversion, required to be mrc format
        """
        self.input_file = input_file
        if not check_image_format(input_file, self.required_input_format):
            raise ValueError("Input image format must be mrc!")

    @property
    def param(self):
        """
        TODO
        This method should return Parameter that needed to run the task
        :return: instance of Param class
        """

    def description(self) -> str:
        """
        TODO
        This method should return the detailed description of the task
        :return: string
        """

    def get_param(self, key: str) -> str:
        """ 
        TODO
        Should provide the Param with name-value pairs 
        """

    def run(self):
        """ Execute two steps to convert and scale the image """

        # Input 


    def get_result(self):
        """ comment """

    def get_logs(self):
        """ comment """