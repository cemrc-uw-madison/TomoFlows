import typing
import subprocess
import os
from program.task import Task

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

    def addArguments(self, args):
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

    def motionCorrectEer(self, in_eer, out_mrc, fmIntFilePath, EEROpts):
        ''' Given EER and mdoc describing file do motion correction '''

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
        
        args = self.AddArguments(args)

        subprocess.call(args)
        # NOTE observed that EER processing results in a flip to be corrected.

    def motionCorrectTiff(self, in_tiff, out_mrc, pixelSize, motionOptions, gain = None):
        ''' Given TIFF or MRC inputs, do motion correction '''

        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

        args = ['motioncor2', "-InTiff", in_tiff, "-OutMrc", out_mrc]
        args = self.AddArguments(args)
        subprocess.call(args)

    def run(self):
        """ This should motion correct a set of micrographs """

        # Input:
        #  - set of input files
        #  - gain file (if provided)
        #  - options related to motion correction parameters

        # Output:
        #  - set of output.mrc files
        #  - log files
        #  - metadata describing the list of output.mrc files.

        # Skeleton 
        infile = ''
        outfile = ''

        # Output is an MRC format, final image size should be 5760x4092 pixels.
        # TODO: build a results.json file and serialize to disk.
        #  can keep the results.json in the class as a member.

    def name(self) -> str:
        return "Motion Correction"

    def description(self) -> str:
        return 'Motion Correction via UCSF MotionCor2'