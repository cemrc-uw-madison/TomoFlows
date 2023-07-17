import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

import scripts.program.scripts_constants as CONSTANTS

def getAngle( fn ):
    try:
        name, num = fn.rsplit('_',1)  # split at the rightmost `_`
        num = num.split('.')[0]
        return int(num)
    except ValueError: # no _ in there
        return fn, None
    
def list_suffix(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

class TaskGenerateStack(Task):
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

    def __createTextStack(self, tiltDirectory, inputFileList, outputText, outputTilt):
        ''' Given a list of filenames, sort by their suffix describing angle and create text index '''

        # Try to get sorting working
        angleList = list(map(lambda x: getAngle(x), inputFileList))
        angleList = sorted(angleList)

        ''' Check the min and max angles '''
        minAngle = min(angleList)
        maxAngle = max(angleList)

        with open(outputTilt, 'w') as file2:
            for angle in angleList:
                file2.write('{:7.2f}\n'.format(angle))

        # Write this to TextStack filename
        tiltList = sorted(inputFileList, key=getAngle)
        lines = list(map(lambda x: os.path.join(tiltDirectory, x + '\n'), tiltList))

        # Format for the text should be:
        # number of input files
        # name of first file to read
        # list of sections to read from first file
        # name of second file to read
        # list of sections to read from second file

        numberFiles = len(lines)

        with open(outputText, 'w') as file1:
            file1.write(str(numberFiles) + '\n')
            for line in lines:
                file1.write(line)
                file1.write('0\n')

        return True
    
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

    def __assemble(self, tiltDirectory, files, outputStack, motionOptions):
        ''' Given that there are several .mrc in directory, create a new stack '''
        if len(files) > 1: 
            # 1. Create the index file 
            txt = os.path.join(tiltDirectory, 'stackIndex.txt') # should use a temp directory?
            tilt = os.path.join(tiltDirectory, 'rawtlt.txt')
            complete = self.__createTextStack(tiltDirectory, files, txt, tilt)
            
            # 2. Create new stack
            if complete:
                self.__createNewStack(txt, tilt, outputStack, motionOptions)
            else:
                print('tilt incomplete, skipping assembly: ' + tiltDirectory)

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

        results_image_meta = ImageMetadata()

        # Iterate through the image_meta, making a stack for each tilt-series.
        for image_set in input_image_meta.image_sets:
            # Get header and images
            header = image_set['header']

            # Get the images to combine as a stack
            imageset_ID = header[CONSTANTS.HEADER_IMAGESET_NAME]
            images = image_set['images']

            # Create an output stack for each tilt-series.
            current_imageset = ImageSet(header, images)
            
            # Create a subfolder for each, for stack and associated text files.
            stack_folder = os.path.join(self.task_folder, CONSTANTS.DATA_SUBFOLDER, imageset_ID, str(imageset_ID))
            if not os.path.isdir(stack_folder):
                os.makedirs(stack_folder)

            stack_path = os.path.join(stack_folder, str(imageset_ID) + '.st')
            images.append(stack_path)

            # the list of images needs to be reorganized by tilt-degree and assembled.
            self.__assemble(images, stack_path)
    
            # then this can be used to build a stack.
            # the stack needs to be described as an output file.
            results_image_meta.add_image_set(current_imageset)

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
