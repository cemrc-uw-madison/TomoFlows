import typing
import subprocess
import os
from scripts.program.metadata.image_metadata import ImageMetadata, ImageSet
from scripts.program.metadata.task_metadata import TaskDescription, TaskOutputDescription
from scripts.program.task import Task

import scripts_constants

def list_suffix(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

class TaskImport(Task):
    """
    Run an import a folder:
     1. folder containing .mdoc that describes each tilt-series data.
      - or -
     2. frames subfolders, each containing a separate tilt-series.

    It will create a TaskDescription, TaskOutputDescription, and ImageDataMetadata
    
    User should specify to "import from mdoc" or "import from frames"
    """

    # Parameters should include import_data: path to a directory of data to import
    # Parameters should include import_directory_type: ['frames' or 'stack'] 
    parameters = {}

    def __init__(self, task_folder):
        """
        :param task_folder: a folder where the task is located on disk.
        """
        self.task_folder = task_folder

    def __find_mdoc(self, directory):
        ''' Find all the mdoc files '''
        # [TODO - this will support ]

    def __read_mdoc(self):
        ''' Read the mdoc files '''

    def __import_from_stacks(self, path_to_stacks):
        """
        :param path_to_stacks: relative path to find the folder containing stacks (.st) and (.mdoc) information.

        Import script that would create the Import job metadata from a "royal stack folder" 
        """
        # [TODO]
        # 1. scan the directory for the .st or .mdoc files
        # 2. each mdoc file should then be attempted to be imported with the job
        # 3. the mdoc will need to be reparsed to pull out the critical information.

    def __import_from_frames(self, path_to_frames):
        """
        :param path_to_frames: relative path to find the folder containing tilt-series information.
        Import script that would create Import job metadata from a "frames folder"
        """
        
        imageMD = ImageMetadata()

        # TODO: 'gain' image files should be excluded from below, and identified uniquely.

        # 1. find each subdirectory containing image files, then finding the files to 'import'
        for childDir in os.listdir(path_to_frames):
            relativePath = os.path.join(path_to_frames, childDir)
            imageset_id = childDir
            if (os.path.isdir(relativePath)):
                image_list = []
                # 2. find all *.tiff, *.eer, or *.mrc files in this folder with accompaning .mdoc information.
                files = list_suffix(relativePath, "tif")
                for f in files:
                    filePath = os.path.join(relativePath, f)
                    image_list.append(filePath)
                files = list_suffix(relativePath, "eer")
                for f in files:
                    filePath = os.path.join(relativePath, f)
                    image_list.append(filePath)
                files = list_suffix(relativePath, "mrc")
                for f in files:
                    filePath = os.path.join(relativePath, f)
                    image_list.append(filePath)
                if len(image_list) > 0:
                    # 3. add the tilt-series ImageSet into imageMD
                    header = {}
                    header[scripts_constants.HEADER_IMAGESET_NAME] = imageset_id
                    tiltset = ImageSet(header, image_list)
                    imageMD.add_image_set(tiltset)

        # Need to save the image metadata, then can include as a result.
        image_json_path = os.path.join(self.task_folder, self.imageset_filename)
        imageMD.save_to_json(image_json_path)
        results = TaskOutputDescription(self.name(), self.description())
        results.add_output_file(image_json_path, 'json')
        return results

    def run(self):
        """ Should run the import task """
        if not self.parameters['import_data']:
            raise ValueError("Parameter 'import_data' is not provided")
        if not self.parameters['import_directory_type']:
            raise ValueError("Parameter 'import_directory_type' is not provided")

        # Create a TaskDescription with parameters.
        task_meta = TaskDescription(self.name(), self.description())
        # Add the Task parameters.
        task_meta.add_parameter('import_data', self.parameters['import_data'])
        task_meta.add_parameter('import_directory_type', self.parameters['import_directory_type'])
        # Create Task folder if missing.
        if not os.path.isdir(self.task_folder):
            os.makedirs(self.task_folder)
        # Serialize the Task description metatadata
        task_meta.save_to_json(os.path.join(self.task_folder, self.task_json))

        # Import the datafiles, building imageset.json and results.json
        results = None
        if self.parameters['import_directory_type'] == 'frames':
            results = self.__import_from_frames(self.parameters['import_data'])
        elif self.parameters['import_directory_type'] == 'stack':
            results = self.__import_from_stacks(self.parameters['import_data'])

        #  Serialize the `result.json` metadata file that points to `imageset.json`
        results_json_path = os.path.join(self.task_folder, self.result_json)
        results.save_to_json(results_json_path)

    def name(self) -> str:
        return "Import"

    def description(self) -> str:
        return 'Import micrographs into a project'
