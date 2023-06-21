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


class TaskAreTomo(Task):
    """
    Run the AreTomo (GPU accelerated) tomogram generation from an image stack
    """

    required_input_format = "mrc"
    required_output_format = "mrc"

    def __init__(self, task_folder):
        """
        :param task_folder: where to write output for the task
        """

    def run(self):
        """ Execute AreTomo for each tilt-series """

    def name(self) -> str:
        return 'AreTomo'
    
    def description(self) -> str:
        return 'Build a tomogram for each tilt-series with `AreTomo`'