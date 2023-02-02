import typing
from task import Task
import subprocess

class TaskGain(Task):
    """
    Initially this can focus on conversion of dm4 to mrc format.

    1. A parameter is the input image file to convert.  (Expect something like 'path-to/gain.dm4')
    2. A parameter to describe how it is scaled
    """

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

        """
        TODO - this should get parameters from Param
        """

        # Input file is DM4 format, initial image size is super-resolution is 11520x8184

        # Skeleton 
        infile = ''
        outfile = ''

        # 1. Convert a format (DM4) to (MRC)
        command1 = 'dm2mrc'
        args = [command1,
            infile,   # Input file could be passed as a parameter 
            outfile]  # Output file should be saved within the job directory <gain.mrc or other>

        stack_infile = ''
        stack_outfile = ''

        # 2. Shrink a gain reference to a different format
        command2 = 'newstack'
        args = [command2,
            '-format', 
            'mrc',
            '-shrink',
            '2',
            '-input',
            stack_infile,
            '-output', 
            stack_outfile]
        subprocess.call(args)

        # Output is an MRC format, final image size should be 5760x4092 pixels.

    def get_result(self):
        """ comment """

    def get_logs(self):
        """ comment """
