import os   
import sys
import argparse

from scripts.program.task_import import TaskImport
from scripts.program.task_motioncor2 import TaskMotionCor2
from scripts.program.metadata.workflow_metadata import WorkflowMetadata

import scripts.program.scripts_constants as CONSTANTS

def run_pipeline(workflow, output_directory):
    """
    Run the steps of the pipeline; external from UI, for testing and development.
    """

    # Create output folder if missing.
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    # 1. task_import
    task1_directory = os.path.join(output_directory, "task_01_import")
    task_import = TaskImport(task1_directory)

    task1 = workflow.tasks[0]
    task1_parameters = task1['parameters']
    print('Task Import parameters: ' + str(task1_parameters) + '\n')
    for key,value in task1_parameters.items():
        task_import.set_parameter(key, value)

    # TaskImport results will include { imageset.json, result.json, task.json }
    task_import.run()

    # 2. task_motioncor2 
    task2_directory = os.path.join(output_directory, "task_02_motioncor2")
    task_motioncor2 = TaskMotionCor2(task2_directory)

    task2 = workflow.tasks[1]
    task2_parameters = task2['parameters']
    print('Task MotionCor2 parameters: ' + str(task2_parameters) + '\n')
    for key,value in task2_parameters.items():
        task_motioncor2.set_parameter(key, value)

    # link to prior task results.
    task_motioncor2.set_parameter('imageset', os.path.join(task1_directory, CONSTANTS.IMAGESET_JSON))

    # TaskMotionCor2 results will include { imageset.json, result.json, task.json, /data/*mrc }
    task_motioncor2.run()


## This is a helper utility to run all the tasks for a data collection
## This runner will be used for the initial code port; testing; review.
def main():
    # 1. Provide command-line arguments
    parser = argparse.ArgumentParser(description='Prepare tilt-series data for use')
    parser.add_argument('--workflow', help='workflow.json describing a task run')
    parser.add_argument('--outputDirectory', help='directory to deposit results', required=True)

    args = parser.parse_args()
    
    workflow = WorkflowMetadata.load_from_json(args.workflow)

    # 2. Creates a new project folder, then builds task folder for each step.
    run_pipeline(workflow, args.outputDirectory)

if __name__ == "__main__":
    main()