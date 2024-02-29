import typing
import subprocess
import os
import uuid
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task
import scripts.program.scripts_constants as CONSTANTS

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
    task_id = uuid.uuid4()
    task_folder = ''

    def __init__(self, task_folder):
        """
        :param input_file: file name in format conversion, required to be dm4 format
        output_file will always be input_file name with mrc extension
        """
        self.task_folder = task_folder

    def run(self):
        """ Execute two steps to convert and scale the image """
        self.logs = []
        self.add_log("Running Gain task...")
        if not os.path.isdir(self.task_folder):
            os.makedirs(self.task_folder)
    
        try:
            if not 'input_file' in self.parameters.keys():
                raise ValueError("Parameter 'Input File' is not provided")
            if not self.parameters['input_file']:
                raise ValueError("Parameter 'Input File' is not provided")
            if not check_image_format(self.parameters['input_file'], self.required_input_format):
                raise ValueError("Input image format must be dm4!")
        except ValueError as err:
            self.add_log("Parameter check failed: " + str(err))
            self.add_log("Gain task run failed")
            results_json_path = os.path.join(self.task_folder, self.result_json)
            results = TaskOutputDescription(self.name(), self.description())
            results.set_status(CONSTANTS.TASK_STATUS_FAILED)
            results.add_errors({"type": "ValueError", "detail": str(err)})
            results.logs = self.logs
            results.save_to_json(results_json_path)
            return

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())
        # TODO: might need to be changed to instead reference the TaskImport (result.json) to find gain images.
        # TODO: external use could provide "parameters" task_meta.add_parameter("input", self.input_file)
        # TODO: this should be serialized to a task directory.

        # Serialize the Task description metatadata
        task_meta.save_to_json(os.path.join(self.task_folder, self.result_json))

        # Input file is DM4 format, initial image size is super-resolution is 11520x8184

        # Skeleton
        infile = self.parameters['input_file']
        outfile = infile.split(".")[0] + ".mrc"

        # 1. Convert a format (DM4) to (MRC)
        command1 = 'dm2mrc'
        args_dm2mrc = [command1,
                infile,   # Input file could be passed as a parameter
                outfile]  # Output file should be saved within the job directory <gain.mrc or other>
        
        # 1. Alternative: Convert a format (.gain/.tiff) to (MRC)
        # use this instead of extension is '.gain'
        command_tiff2mrc = 'tiff2mrc'
        args_tiff2mrc = [command1,
                infile,   # Input file could be passed as a parameter
                outfile]  # Output file should be saved within the job directory <gain.mrc or other>

        subprocess.call(args_dm2mrc)

        # [TODO]
        # We should have a parameter about expected output size (5k x 4k) or (4k x 4k)
        # We should check the outfile to see if it matches or needs to be downscaled
        # If needs to downscale -> see below 

        # 2. Shrink a gain reference to a different format
        stack_infile = outfile
        stack_outfile = f"{infile.split('.')[0]}-Shrink.mrc"
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

        # TODO: write also results here.
        self.add_log("Import task run completed successfully")
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results = TaskOutputDescription(self.name(), self.description())
        results.set_status(CONSTANTS.TASK_STATUS_SUCCESS)
        results.logs = self.logs
        results.save_to_json(results_json_path)

    def name(self) -> str:
        return "Gain"

    def description(self) -> str:
        return 'Conversion of gain file formats'
