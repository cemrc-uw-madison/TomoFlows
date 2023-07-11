import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

import scripts.program.scripts_constants as CONSTANTS

class generate_stack(Task):
    """
    Run `newstack` to assemble a stack
    """

    required_input_format = "mrc"
    required_output_format = "mrc"

    def __init__(self, task_folder):
        """
        :param task_folder: where to create the task folder
        """
        self.task_folder = task_folder

    def name(self) -> str:
        return "Assemble stacks (newstack)"

    def description(self) -> str:
        return 'Create ordered image stacks for each tilt-series'
    
    def __createNewStack(self, inputFileList, rawtlt, outputFile, postRotation = None):
        """ Create a stack of images, using text files of tilt angles and of input files """
        # Example: newstack -tilt AlignedStack_fcor.rawtlt -fileinlist inputfile_3degreeincrement.txt AlignedStack_fcor.st
        command = 'newstack'
        args = [ command,
        #    '-UseMdocFiles',
            '-tilt', rawtlt,
            '-fileinlist', inputFileList,
            outputFile
        ]

        # rotate images if needed. ie, for the Krios G4 Falcon4.
        if postRotation:
            args.append('-rotate')
            args.append(postRotation)

        subprocess.call(args)

    def __alterHeader(self, stackFile, tiltAxisAngle, binning):
        """ Add a header text line describing the tilt axis angle """
        # Example: alterheader AlignedStack_fcor.st -ti "Tilt axis angle = 86.0, binning = 1"
        header = 'Tilt axis angle = {:3.2f}, binning = {:.1f}'.format(tiltAxisAngle, float(binning))    
        command = 'alterheader'
        args = [ command,
            stackFile,
            '-ti', header
        ]
        subprocess.call(args)
        print("Added header information: " + header)

    def run(self):
        """ Execute newstack for each tilt-series """
        # Input:
        #  - set of input files

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())
        task_meta.add_parameters(self.parameters)
        
        # Create Task folder if missing.
        if not os.path.isdir(self.task_folder):
            os.makedirs(self.task_folder)
        # Serialize the Task description metatadata
        task_meta.save_to_json(os.path.join(self.task_folder, self.task_json))

        # Require an imageset containing *.mrc (stack) files
        input_image_meta = None
        if 'imageset' in self.parameters:
            task_meta.add_parameter('imageset', self.parameters['imageset'])
            imageset_filename = self.parameters['imageset']
            input_image_meta = ImageMetadata.load_from_json(imageset_filename)
        else: 
            raise ValueError("Parameter 'imageset' is not provided")

        # Create Task folder if missing.
        if not os.path.isdir(self.task_folder):
            os.makedirs(self.task_folder)

        results_image_meta = ImageMetadata()

        # Iterate through the image_meta.
        for image_set in input_image_meta.image_sets:
            image_list = []

            # Get header and images
            header = image_set['header']

            # Get the images to combine as a stack
            imageset_ID = header[CONSTANTS.HEADER_IMAGESET_NAME]
            images = image_set['images']

            # TODO:
            # the list of images needs to be reorganized by tilt-degree
            # then this can be used to build a stack.
            # the stack needs to be described as an output file.


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