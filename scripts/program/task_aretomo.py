import typing
import subprocess
import os
from program.task import Task


def check_image_format(file_name, required_format):
    """

    :param file_name: provided file name
    :param required_format: required file format
    :return: if file has required format(Boolean value)
    """
    image_format = file_name.split(".")[-1]
    return image_format == required_format


class TaskAretomo(Task):
    """
    Provide mrc stack to AreTomo, with parameters, to generate a tomogram.
    """

    required_input_format = "mrc"

    def __init__(self, input_file):
        """
        :param input_file: file name in format conversion, required to be dm4 format
        """
        self.input_file = input_file
        if not check_image_format(input_file, self.required_input_format):
            raise ValueError("Input image format must be mrc!")

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

    def run(self):
        """ Execute two steps to convert and scale the image """

        # infile, outfile, AngFile=None, voltage=300, pixelSize=1.4, TiltRangePos=None, TiltRangeNeg=None, VolZ=1500, OutBin=4, TiltAxisAngle=None
        AreTomo = 'AreTomo'
        inputType = '-InMrc'
        outType = '-OutMrc'
        outFile = os.path.join(self.task_output_folder, 'tomogram.mrc') 

        if (os.path.exists(outfile)):
            print(outfile + ' exists: skipping ' + AreTomo)
        else:
            print(outfile + ' will be created by AreTomo...')

            # AlignZ should always be smaller than VolZ (and temporary volume for aligment)
            AlignZ = int(VolZ * 0.8)

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

            # DarkTol, helps to include all tilts
            # FlipVol to put on conventional orientation
            # Imod provides files to help view in IMOD
            # Patch 4 4 for slower, but maybe better alignment in difficult cases. 

            # Updates 11/29/2022 [TODO]
            # provide the -AngFile with dose values.
            # -Kv also required for the dose weighting   
            # -PixSize in angstrom also required for dose weighting
            # -AlignZ also should be provided as an integer that is 0.8X VolZ.
            # How can user provide the VolZ?

            # Permissions change for the output Imod directory.
            # We should have a 'note.txt' that includes the command that is run.

            # TODO: provide a mechanism that writes executed commands to a text file: print(args)
            subprocess.call(args)

            # Output is an MRC volume 

    def get_result(self):
        """ comment """

    def get_logs(self):
        """ comment """
