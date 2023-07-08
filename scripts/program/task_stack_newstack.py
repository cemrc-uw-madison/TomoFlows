import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

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
        return "Assemble stacks (newstack)"

    def description(self) -> str:
        return 'Create ordered image stacks for each tilt-series'

    def run(self):
        """ Execute newstack for each tilt-series """
        # [TODO]

        # Output:
        #  - set of output.mrc files for each stack
        #  - log files
        #  - image metadata, describing the output mrc files.
        image_json_path = os.path.join(self.task_folder, self.imageset_filename)
        results_image_meta.save_to_json(image_json_path)

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results = TaskOutputDescription(self.name(), self.description())
        results.add_output_file(image_json_path, 'json')
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

