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


class TaskGain(Task):
    """
    Initially this can focus on conversion of dm4 to mrc format.

    1. A parameter is the input image file to convert.  (Expect something like 'path-to/gain.dm4')
    2. A parameter to describe how it is scaled
    """
    required_input_format = "dm4"
    required_output_format = "mrc"

    def __init__(self, input_file):
        """
        :param input_file: file name in format conversion, required to be dm4 format
        output_file will always be input_file name with mrc extension
        """

        if not check_image_format(input_file, self.required_input_format):
            raise ValueError("Input image format must be dm4!")
        self.input_file = input_file
        self.output_file = input_file.split(".")[0] + ".mrc"

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

    def run(self, stack_outfile):
        """ Execute two steps to convert and scale the image """

        """
        TODO - this should get parameters from Param
        """

        # Input file is DM4 format, initial image size is super-resolution is 11520x8184

        # Skeleton
        infile = self.input_file
        outfile = self.output_file

        # 1. Convert a format (DM4) to (MRC)
        command1 = 'dm2mrc'
        args_dm2mrc = [command1,
                infile,   # Input file could be passed as a parameter
                outfile]  # Output file should be saved within the job directory <gain.mrc or other>

        subprocess.call(args_dm2mrc)
        # 2. Shrink a gain reference to a different format
        stack_infile = outfile
        command2 = 'newstack'

        args_newstack = [command2,
                '-format',
                'mrc',
                '-shrink',
                '2',
                '-input',
                stack_infile,
                '-output',
                stack_outfile]
        
        subprocess.call(args_newstack)

        # Output is an MRC format, final image size should be 5760x4092 pixels.

        # 3. Remove temp mrc file
        args_remove = ["rm",
                "-f",
                outfile]
        subprocess.call(args_remove)

    def get_result(self):
        """ comment """

    def get_logs(self):
        """ comment """
