import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
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
        self.task_folder = task_folder

    def __runAreTomo(self, infile, outfile, AngFile=None, voltage=300, pixelSize=1.4, TiltRangePos=None, TiltRangeNeg=None, VolZ=1500, OutBin=4, TiltAxisAngle=None):
        AreTomo = 'AreTomo'
        inputType = '-InMrc'
        outType = '-OutMrc'

        if (os.path.exists(outfile)):
            print(outfile + ' exists: skipping ' + AreTomo)
        else:
            print(outfile + ' will be created by AreTomo...')

            # AlignZ should always be smaller than VolZ (and temporary volume for aligment)
            AlignZ = int(VolZ * 0.8)

            # Build the command.
            args = [AreTomo,
                inputType, infile,
                outType, outfile,
                '-VolZ', str(VolZ),
                '-AlignZ', str(AlignZ),
                '-OutBin', str(OutBin),
                '-DarkTol', str(0.1),
                '-OutImod', str(1),
                '-FlipVol', str(1),
                '-Patch', '4 4',
                '-Kv', str(voltage),
                '-PixSize', str(pixelSize),
                '-Wbp', str(1)
            ]

            if AngFile:
                args.append('-AngFile')
                args.append(str(AngFile))
            else:
                args.append('-TiltRange')
                args.append(str(TiltRangeNeg))
                args.append(str(TiltRangePos))

            if TiltAxisAngle:
                args.append('-TiltCor')
                args.append('0') # no correction, only measurement
                args.append('-TiltAxis')
                args.append(str(TiltAxisAngle))
                args.append(str(1)) # refine input angle at each tilt
        
            subprocess.call(args)

    def __batch_aretomo(self, imagesets):
        """
        Run AreTomo on each of the stacks from an imageset
        """
        results_image_meta = ImageMetadata()
        
        # Iterate through the image_meta.
        for image_set in imagesets:
            # Get header and images
            header = image_set['header']

            # Get the imagesets that each will be built into a tomogram
            imageset_ID = header[CONSTANTS.HEADER_IMAGESET_NAME]
            images = image_set['images']

            # Each image_set should contain only a single stack.mrc
            image = images[0]
            
            aretomo_images = []
            current_imageset = ImageSet(header, aretomo_images)

            # Create a subfolder for each, for tomogram and associated files
            tomogram_folder = os.path.join(self.task_folder, CONSTANTS.DATA_SUBFOLDER, imageset_ID, str(imageset_ID))
            if not os.path.isdir(tomogram_folder):
                os.makedirs(tomogram_folder)

            # This should take the Argument options if provided.
            outfile = os.path.join(tomogram_folder, 'tomogram.mrc')

            # Defaults that are overridden by parameters.
            kV = 300
            if 'Kv' in self.parameters:
                kV = self.parameters['kV']

            pixSize = 1.4
            if 'PixSize' in self.parameters:
                pixSize = self.parameters['PixSize']

            volZ = 1500
            if 'VolZ' in self.parameters:
                volZ =  self.parameters['VolZ']

            outBin = 6
            if 'OutBin' in self.parameters:
                outBin = self.parameters['OutBin']

            # TODO: should this take generate this angfile?
            angFile = None
            if 'angFile' in self.parameters:
                angFile = self.parameters['AngFile']

            # TiltRangePos, TiltRangeNeg (not used anymore)?

            tiltAxisAngle = None
            if 'tiltAxisAngle' in self.parameters:
                tiltAxisAngle = self.parameters['TiltAxisAngle']

            # Should use the AngFile, not TiltRange arguments, consider removing?
            self.__runAreTomo(image, outfile, voltage=kV, pixelSize=pixSize, VolZ=volZ, OutBin=outBin, TiltAxisAngle=tiltAxisAngle, AngFile=angFile, TiltRangePos=None, TiltRangeNeg=None)

            # Add the tomogram to the results
            aretomo_images.append(outfile)
            results_image_meta.add_image_set(current_imageset)

        return results_image_meta

    def run(self):
        """ Execute AreTomo for each tilt-series """

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())

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

        # Add all the required/optional parameters here.
        task_meta.add_parameters(self.parameters)

        # Serialize the Task description metatadata
        task_meta.save_to_json(os.path.join(self.task_folder, self.result_json))

        # Run AreTomo on each of the stacks.
        results_image_meta = self.__batch_aretomo(input_image_meta.image_sets)

        # Output:
        #  - set of output.mrc files for each tomogram
        #  - log files
        #  - image metadata, describing the output mrc files.
        image_json_path = os.path.join(self.task_folder, self.imageset_filename)
        results_image_meta.save_to_json(image_json_path)

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results = TaskOutputDescription(self.name(), self.description())
        results.add_output_file(image_json_path, 'json')
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

    def name(self) -> str:
        return 'Tomogram Generation (AreTomo)'
    
    def description(self) -> str:
        return 'Build a tomogram for each stack with UCSF AreTomo'
