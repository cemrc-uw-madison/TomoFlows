import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

def check_image_format(file_name, required_format):
    """

    :param file_name: provided file name
    :param required_format: required file format
    :return: if file has required format(Boolean value)
    """
    image_format = file_name.split(".")[-1]
    return image_format == required_format


class TaskGctf(Task):
    """
    Run `Gctf` to do CTF estimation on a set of micrographs
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
        
    def __run_gctf(in_mrc, out_mrc, output_EPA, pixelSize):
        """ Run gCTF to provide CTF estimation """

        if (os.path.exists(output_EPA)):
            print(output_EPA + ' exists: skipping gCTF')
        else:
            command = 'Gctf'
            args = [command, '--apix', str(pixelSize), '--kV', str(motionOptions.voltage), '--cs', str(motionOptions.sphericalAberration), '--ac', str(motionOptions.amplitudeContrast), input_mrc]

            # Setup a temporary directory and run Gctf
            with tempfile.TemporaryDirectory() as tmpdirname:
                subprocess.call(args)

    def run(self):
        """ CTF estimation for a list of files """

        # TODO: create a results.json describing the output.

    def name(self) -> str:
        return "CTF Estimation (Gctf)"

    def description(self) -> str:
        return "Perform CTF estimation for each micrograph with Gctf"
