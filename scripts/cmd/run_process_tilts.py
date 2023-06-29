import os   
import sys
import argparse

absolute_path = os.path.dirname(__file__)
absolute_list = absolute_path.split("/")
absolute_list[-1] = "program/"
sys.path.append("/".join(absolute_list))

from task_import import TaskImport
from task_motioncor2 import TaskMotionCor2

def run_pipeline(frames_directory, output_directory):
    """
    Run the steps of the pipeline; external from UI, for testing and development.
    """

    # Create output folder if missing.
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    # 1. task_import, called to accept the "royal stack mdoc to find tilt-series"
    task_directory = os.path.join(output_directory, "task_01_import")
    task_import = TaskImport(task_directory)
    task_import.set_parameter('import_data', frames_directory)
    task_import.set_parameter('import_directory_type', 'frames')
    task_import.run()

    # 2. task_motioncor2, should then be called providing the task_import results to continue.
    import_result = task_import.get_result()
    # The only output_file, from TaskImport should be a JSON file, and 'imageset'
    imported_images = import_result.output_files[0]
    print("Imported images in: " + str(imported_images['file_name']))

    task_directory = os.path.join(output_directory, "task_02_motioncor")
    task_motioncor2 = TaskMotionCor2(task_directory)
    task_motioncor2.set_parameter('PixSize', '4.727')
    task_motioncor2.set_parameter('imageset', imported_images['file_name'])
    task_motioncor2.run()

## This is a helper utility to run all the tasks for a data collection
## This runner will be used for the initial code port; testing; review.
def main():
    # 1. Provide command-line arguments
    parser = argparse.ArgumentParser(description='Prepare tilt-series data for use')
    parser.add_argument('--frames', help='parent directory containing multiple tilt stacks', required=False, default=None)
    parser.add_argument('--outputDirectory', help='directory to deposit results', required=True)

    args = parser.parse_args()

    # 2. Creates a new project folder, then builds task folder for each step.
    run_pipeline(args.frames, args.outputDirectory)

if __name__ == "__main__":
    main()