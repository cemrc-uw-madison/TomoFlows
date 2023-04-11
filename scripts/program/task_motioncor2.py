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

    @property
    def param(self):
        """
        TODO
        This method should return Parameter that needed to run the task
        :return: instance of Param class
        """

    def description(self) -> str:
        """
        TODO
        This method should return the detailed description of the task
        :return: string
        """

    def get_param(self, key: str) -> str:
        """ 
        TODO
        Should provide the Param with name-value pairs 
        """

    def motionCorrectEer(in_eer, fmIntFilePath, EEROpts, out_mrc):
        ''' Given EER and mdoc describing file do motion correction '''
        if (os.path.exists(out_mrc)):
            print(str(out_mrc) + ' exists: skipping motionCor')
        else:
            print(str(out_mrc) + ' will be created by motionCor...')

            motionCor = 'motioncor2'
            inputType = "-InEER"

            # TODO: avoid creating *DW.mrc files.

            args = [motionCor,
                inputType, str(in_eer),
                "-OutMrc", str(out_mrc),
                "-FtBin", "2",
                "-EerSampling", "2",
                "-Patch", "5 5",
                "-Iter", "20",
                "-Tol", "0.5",
                "-Gpu", "0 1 2 3",
                "-Gain", str(EEROpts.gain),
                "--EerSampling", "2",
                "-PixSize", str(EEROpts.pixelSize / 2.0),
                "-FmIntFile", str(fmIntFilePath)]

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

    def get_result(self):
        """ comment """

    def get_logs(self):
        """ comment """