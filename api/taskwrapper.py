import json
import time
import random
import pytz
import os
from datetime import datetime

from scripts.program.task_gain import TaskGain
from scripts.program.task_motioncor2 import TaskMotionCor2
from scripts.program.task_import import TaskImport
from django.conf import settings

import scripts.program.scripts_constants as CONSTANTS

def task_handler(project_task, run):
    if project_task.task.name == "Gain":
        task_gain_handler(project_task, run)
    elif project_task.task.name == "Motion Correction (MotionCor2)":
        task_motioncor2_handler(project_task, run)
    elif project_task.task.name == "Import":
        task_import_handler(project_task, run)
    else:
        task_sample_handler(project_task, run)

def task_sample_handler(project_task, run):
    time.sleep(10)
    choice = random.choice(["SUCCESS", "FAILED"])
    run.status = choice
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    if choice == "SUCCESS":
        run.logs = json.dumps([
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Running sample task...",
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": f"Parameter values received: {json.loads(project_task.parameter_values)}",
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Waiting for 10s"
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Sample task run completed successfully"
            },
        ])
        run.errors = json.dumps([])
    else:
        run.logs = json.dumps([
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Running sample task..."
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": f"Parameter values received: {json.loads(project_task.parameter_values)}",
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Waiting for 10s"
            },
            {
                "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
                "detail": "Sample task run failed. Check errors for more information"
            }
        ])
        run.errors = json.dumps([
            {
                "type": "Server Error",
                "detail": "Sampele task run programmed to fail or succeed randomly"
            }
        ])
    run.save()
        
def task_gain_handler(project_task, run):
    project = project_task.project
    # TODO: ideally parameters would provide name:value pairs as a dictionary? We only get the values.
    parameters = json.loads(project_task.parameter_values)
    input_file = parameters[0]

    logs = []
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Running Gain task...",
    })

    project_folder = os.path.join( project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id) )

    task_gain = TaskGain(project_folder, input_file)
    task_gain.run()

    run.status = task_gain.get_result().status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Gain task run completed successfully"
    })
    run.logs = json.dumps(logs)
    run.errors = json.dumps([])
    run.save()

def task_motioncor2_handler(project_task, run):
    project = project_task.project
    # TODO: ideally parameters would provide name:value pairs as a dictionary? We only get the values.
    parameters = json.loads(project_task.parameter_values)

    logs = []
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Running Motion Correction (MotionCor2) task...",
    })
    
    project_folder = os.path.join( project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id) )
    task_motioncor2 = TaskMotionCor2(project_folder)
    # TODO: add the parameters here
    task_motioncor2.run()
    
    run.status = task_motioncor2.get_result().status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Motion Correction (MotionCor2) task run completed successfully"
    })
    run.logs = json.dumps(logs)
    run.errors = json.dumps([])
    run.save()

def task_import_handler(project_task, run):
    project = project_task.project
    # TODO: ideally parameters would provide name:value pairs as a dictionary? We only get the values.
    parameters = json.loads(project_task.parameter_values)

    project_folder = os.path.join( project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id) )
    print("Will create at: " + project_folder)

    print(parameters)
    task_import = TaskImport(project_folder)
    # TODO: if we can get name:value dictionary from the JSON string, this could be simplified here?
    task_import.parameters['import_data'] = parameters[0]
    task_import.parameters['import_directory_type'] = parameters[1]
    task_import.run()
    
    result = task_import.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.save()
