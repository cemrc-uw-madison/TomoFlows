import typing
import subprocess
import os

from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

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

    def __batch_aretomo(self, imageset):
        """
        Run AreTomo on each of the stacks from an imageset
        """
        results = TaskOutputDescription(self.name(), self.description())
        
        # [TODO] - make the runner on all the stacks here.
        # add each of the resulting tomograms into a result.json file.
        # return this as the result of the method.

    def run(self):
        """ Execute AreTomo for each tilt-series """

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())
        # Add the Task parameters.
        # Require an imageset containing *.mrc (stack) files
        imageset = None
        if 'imageset' in self.parameters.keys:
            task_meta.add_parameter('imageset', self.parameters['imageset'])
            iamgeset_filename = self.parameters['imageset']
        else: 
            raise ValueError("Parameter 'imageset' is not provided")

        # Create Task folder if missing.
        if not os.path.isdir(self.task_folder):
            os.path.mkdirs(self.task_folder)

        # Add all the required/optional parameters here.
        if 'VolZ' in self.parameters.keys:
            task_meta.add_parameter('VolZ', self.parameters['VolZ'])
        if 'AlignZ' in self.parameters.keys:
            task_meta.add_parameter('AlignZ', self.parameters['AlignZ'])
        if 'OutBin' in self.parameters.keys:
            task_meta.add_parameter('OutBin', self.parameters['OutBin'])
        if 'DarkTol' in self.parameters.keys:
            task_meta.add_parameter('DarkTol', self.parameters['DarkTol'])
        if 'OutImod' in self.parameters.keys:
            task_meta.add_parameter('OutImod', self.parameters['OutImod'])
        if 'FlipVol' in self.parameters.keys:
            task_meta.add_parameter('FlipVol', self.parameters['FlipVol'])
        if 'Patch' in self.parameters.keys:
            task_meta.add_parameter('Patch', self.parameters['Patch'])
        if 'Kv' in self.parameters.keys:
            task_meta.add_parameter('Kv', self.parameters['Kv'])           
        if 'PixSize' in self.parameters.keys:
            task_meta.add_parameter('PixSize', self.parameters['PixSize'])
        if 'Wbp' in self.parameters.keys:
            task_meta.add_parameter('Wbp', self.parameters['Wbp'])
        # This provides what are the tilt angles in the stack for each image layer.
        if 'AngFile' in self.parameters.keys:
            task_meta.add_parameter('AngFile', self.parameters['AngFile']) 
        # Alternative to AngFile is to provide a TiltRange. 
        if 'TiltRange' in self.parameters.keys:
            task_meta.add_parameter('TiltRange', self.parameters['TiltRange'])    
        if 'TiltCor' in self.parameters.keys:
            task_meta.add_parameter('TiltCor', self.parameters['TiltCor'])            
        if 'TiltAxisAngle' in self.parameters.keys:
            task_meta.add_parameter('TiltAxisAngle', self.parameters['TiltAxisAngle'])      
        # Serialize the Task description metatadata
        task_meta.save_to_json(os.path.join(self.task_folder, self.result_json))

        # Run AreTomo on each of the stacks.
        results = self.__batch_aretomo(imageset)

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

    def name(self) -> str:
        return 'Tomogram Generation (AreTomo)'
    
    def description(self) -> str:
        return 'Build a tomogram for each stack with UCSF AreTomo'
