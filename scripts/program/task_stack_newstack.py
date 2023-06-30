import typing
import subprocess
import os
from program.task import Task

class generate_stack(Task):
    """
    Run `newstack` to assemble a stack
    """

    required_input_format = "mrc"
    required_output_format = "mrc"

    def __init__(self, input_file):
        """
        """

    def name(self) -> str:
        return "Alignframes"

    def description(self) -> str:
        return 'Build a stack for each tilt-series with `newstack`'

    def run(self):
        """ Execute newstack for each tilt-series """
        # [TODO]

