import os   
import sys
import argparse

from scripts.program.task_import import TaskImport
from scripts.program.task_motioncor2 import TaskMotionCor2
from scripts.program.metadata.workflow_metadata import WorkflowMetadata

## This is a helper utility to run all the tasks for a data collection
## This runner will be used for the initial code port; testing; review.
def main():
    workflow = WorkflowMetadata()

    # Import
    task1_params = {
        "import_data": '/mnt/scratch/mrlarson2/test',
        "import_directory_type": "frames"
    }

    # Motion Correction
    task2_params = {
        "PixSize": "4.727",
        'Patch': '5 5'
    }

    # Stack Generation
    task3_params = {
    }

    # AreTomo
    task4_params = {
    }

    workflow.add_task("task1", task1_params)
    workflow.add_task("task2", task2_params)
    workflow.add_task("task3", task3_params)
    workflow.add_task("task4", task4_params)

    workflow.save_to_json("example_workflow.json")

if __name__ == "__main__":
    main()
