import typing
import subprocess
import os

from metadata.image_metadata import ImageMetadata, ImageSet
from metadata.task_metadata import TaskDescription, TaskOutputDescription
from task import Task

class TaskMotionCor2(Task):
    """
    This task would motion correct micrograph movies (MRC, TIF, or EER as valid input formats)
    """
    required_input_formats = ["mrc", "tif", "tiff", "eer" ]
    required_output_format = "mrc"

    # Parameters should include gain filename.
    # Parameters should include a list of input files to motion correct.

    def __init__(self, task_folder):
        """
        :param task_folder: where to create the task folder
        """
        self.task_folder = task_folder

    def __addArguments(self, args):
        """ Append any motion correction required or optional arguments """

        # Required parameters
        if self.parameters['PixSize']:
            args.append('-PixSize')
            args.append(str(self.parameters['PixSize']))
        else:
            raise ValueError('-PixSize: Missing')
        
        if self.parameters['Patch']:
            args.append('-Patch')
            args.append(str(self.parameters['Patch']))
        else:
            raise ValueError('-Patch: Missing')

        # Optional parameters
        if self.parameters['Iter']:
            args.append('-Iter')
            args.append(str(self.parameters['Iter']))

        if self.paramters['Tol']:
            args.append('-Tol')
            args.append(str(self.parameters['Tol']))   

        if self.parameters['Gpu']:
            args.append('-Gpu')
            args.append(str(self.parameters['Gpu']))

        if self.parameters['Gain']:
            args.append('-Gain')
            args.append(str(self.parameters['Gain']))

        if self.parameters['RotGain']:
            args.append("-RotGain")
            args.append(str(self.parameters['RotGain']))

        if self.parameters['FlipGain']:
            args.append("-FlipGain")
            args.append(str(self.parameters['FlipGain']))

        if self.parameters['Throw']:
            args.append("-Throw")
            args.append(str(self.parameters['Throw']))

        if self.parameters['-FtBin']:
            args.append("-FtBin")
            args.append(str(self.parameters['-FtBin']))
            # NOTE: may need to be combined with use of PixSize / 2.

        return args

    def __motionCorrectEer(self, in_eer, out_mrc, fmIntFilePath, EEROpts):
        """ Given EER and mdoc describing file do motion correction """

        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

        args = ['motioncor2', "-InEER", in_eer, "-OutMrc", out_mrc]
        
        # EER specific options, required if EER.
        if self.parameters['-FmIntFile']:
            args.append('-FmIntFile')
            args.append(str(self.parameters['FmIntFile']))
        else:
            raise ValueError('-FmIntFile: Missing') 

        if self.parameters['-EerSampling']:
            args.append("-EerSampling")
            args.append(str(self.parameters['EerSampling']))
        else:
            raise ValueError('-EerSampling: Missing') 
        
        if self.parameters['-FtBin']:
            args.append("-FtBin")
            args.append(str(self.parameters["FtBin"]))
        else:
            raise ValueError('-FtBin: Missing')
        
        args = self.__addArguments(args)

        subprocess.call(args)
        # NOTE observed that EER processing results in a flip to be corrected.

    def __motionCorrectTiff(self, in_tiff, out_mrc):
        """ Given TIFF or MRC inputs, do motion correction """

        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

        args = ['motioncor2', "-InTiff", in_tiff, "-OutMrc", out_mrc]
        args = self.__addArguments(args)
        subprocess.call(args)

    def run(self):
        """ This should motion correct a set of micrographs """
        # Input:
        #  - set of input files
        #  - gain file (if provided)
        #  - options related to motion correction parameters

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())
        # Add the Task parameters.
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
            for image in image_set['images']:
                if image.endswith('.' + '.tif'):
                    outfile = image[:-len('.tif')] + '.mc.mrc'
                    # self.__motionCorrectTiff(image, outfile)
                    # [TODO] : processing step
                    image_list.append(outfile)
                if image.endswith('.' + '.eer'):
                    outfile = image[:-len('.eer')] + '.mc.mrc'
                    # [TODO] : processing step
                    image_list.append(outfile)
                if image.endswith('.' + '.mrc'):
                    outfile = image[:-len('.mrc')] + '.mc.mrc'
                    # [TODO] : processing step
                    image_list.append(outfile)

            if len(image_list) > 0:
                # add the motion-corrected images into metadata for the task.
                header = {}
                tiltset = ImageSet(header, image_list)
                results_image_meta.add_image_set(tiltset)

        # Output:
        #  - set of output.mrc files
        #  - log files
        #  - image metadata, describing the output mrc files.
        image_json_path = os.path.join(self.task_folder, self.imageset_filename)
        results_image_meta.save_to_json(image_json_path)

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results = TaskOutputDescription(self.name(), self.description())
        results.add_output_file(image_json_path, 'json')
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

    def name(self) -> str:
        return "Motion Correction"

    def description(self) -> str:
        return 'Motion Correction via UCSF MotionCor2'