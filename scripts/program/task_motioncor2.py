import typing
import subprocess
import os

from scripts.program.mdoc import MDoc, FrameSet
import scripts.program.processEER

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

import scripts.program.scripts_constants as CONSTANTS
import scripts.program.processEER as processEER

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
        if 'PixSize' in self.parameters:
            args.append('-PixSize')
            args.append(str(self.parameters['PixSize']))
        else:
            raise ValueError('-PixSize: Missing')
        
        if 'Patch' in self.parameters:
            args.append('-Patch')
            args.append(str(self.parameters['Patch']))
        else:
            raise ValueError('-Patch: Missing')

        # Optional parameters
        if 'Iter' in self.parameters:
            args.append('-Iter')
            args.append(str(self.parameters['Iter']))

        if 'Tol' in self.parameters:
            args.append('-Tol')
            args.append(str(self.parameters['Tol']))   

        if 'Gpu' in self.parameters:
            args.append('-Gpu')
            args.append(str(self.parameters['Gpu']))

        if 'Gain' in self.parameters:
            args.append('-Gain')
            args.append(str(self.parameters['Gain']))

        if 'RotGain' in self.parameters:
            args.append("-RotGain")
            args.append(str(self.parameters['RotGain']))

        if 'FlipGain' in self.parameters:
            args.append("-FlipGain")
            args.append(str(self.parameters['FlipGain']))

        if 'Throw' in self.parameters:
            args.append("-Throw")
            args.append(str(self.parameters['Throw']))

        if 'FtBin' in self.parameters:
            args.append("-FtBin")
            args.append(str(self.parameters['FtBin']))
            # NOTE: may need to be combined with use of PixSize / 2.

        return args

    def __motionCorrectEer(self, in_eer, out_mrc, fmIntFilePath, EEROpts):
        """ Given EER and mdoc describing file do motion correction """

        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

        args = ['motioncor2', "-InEER", in_eer, "-OutMrc", out_mrc]

        # EER processing requires an FmIntFile, by default we should auto-generate this.
        if 'FmIntFile' in self.parameters:
            args.append('-FmIntFile')
            args.append(str(self.parameters['FmIntFile']))
        else:
            args.append('-FmIntFile')
            args.append(str(fmIntFilePath))

        defaultBin = True
        if 'EerSampling' in self.parameters:
            args.append("-EerSampling")
            args.append(str(self.parameters['EerSampling']))
            defaultBin = False
        
        if 'FtBin' in self.parameters:
            args.append("-FtBin")
            args.append(str(self.parameters["FtBin"]))
            defaultBin = False

        if defaultBin:
            # Upsampling + Fourier Cropping may be a good default.
            args.append('-EerSampling')
            args.append(str(2))
            args.append('-FtBin')
            args.append(str(2))
        
        args = self.__addArguments(args)

        print (args)
        # subprocess.call(args)
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

    def __motionCorrectMRC(self, in_mrc, out_mrc):
        """ Given TIFF or MRC inputs, do motion correction """

        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

        args = ['motioncor2', "-InMRC", in_mrc, "-OutMrc", out_mrc]
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

        # Iterate through the image_meta.
        for image_set in input_image_meta.image_sets:
            image_list = []

            header = image_set['header']

            # Get header and images
            imageset_ID = header[CONSTANTS.HEADER_IMAGESET_NAME]
            images = image_set['images']
            
            # Prepare output folder
            out_folder = os.path.join(self.task_folder, CONSTANTS.DATA_SUBFOLDER, imageset_ID)
            if not os.path.isdir(out_folder):
                os.makedirs(out_folder)

            for image in images:
                print(image + '\n')
                filename = os.path.basename(image)
                if image.endswith('.tif'):
                    outfile = os.path.join(out_folder, filename[:-len('.tif')] + '.mc.mrc')
                    self.__motionCorrectTiff(image, outfile)
                    image_list.append(outfile)
                elif image.endswith('.mrc'):
                    outfile = os.path.join(out_folder, filename[:-len('.mrc')] + '.mc.mrc')
                    self.__motionCorrectMRC(image, outfile)
                    image_list.append(outfile)
                elif image.endswith('.eer'):
                    outfile = os.path.join(out_folder, filename[:-len('.eer')] + '.mc.mrc')

                    # read the associated mdoc file
                    mdoc_filename = image + '.mdoc'
                    EEROpts = processEER.readMdoc(mdoc_filename)

                    # preparse an FmIntFile.txt
                    dosefile = os.path.join(out_folder, 'FmIntFile.txt')
                    processEER.prepareIntFile(image, EEROpts.exposureDose, dosefile)

                    # [TODO]: replace with the task that does gain reference conversions?
                    # Convert gain if needed from .tiff -> .mrc format.
                    # This mechanism to find the gain file depends on SerialEM MDOC
                    parent_folder = os.path.dirname(os.path.realpath(image))
                    gain_infile = EEROpts.gain
                    gain_inpath = os.path.join(parent_folder, EEROpts.gain)
                    gain_mrc = os.path.join(out_folder, 'gain.mrc')
                    processEER.convertTifMrc(gain_inpath, gain_mrc)
                    EEROpts.gain = gain_mrc
                    self.__motionCorrectEer(image, outfile, dosefile, EEROpts)
                    
                    image_list.append(outfile)
                else:
                    print('Unable to process image: ' + image)

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
        return "Motion Correction (MotionCor2)"

    def description(self) -> str:
        return 'Motion Correction of micrographs via UCSF MotionCor2'
