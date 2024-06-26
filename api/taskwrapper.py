import json
import time
import random
import pytz
import os
from datetime import datetime

from scripts.program.task_gain import TaskGain
from scripts.program.task_motioncor2 import TaskMotionCor2
from scripts.program.task_motioncor3 import TaskMotionCor3
from scripts.program.task_stack_newstack import TaskGenerateStack
from scripts.program.task_import import TaskImport
from scripts.program.task_aretomo import TaskAreTomo
from django.conf import settings

import scripts.program.scripts_constants as CONSTANTS

def task_handler(project_task, run):
    if project_task.task.name == "Gain":
        task_gain_handler(project_task, run)
    elif project_task.task.name == "Motion Correction (MotionCor2)":
        task_motioncor2_handler(project_task, run)
    elif project_task.task.name == "Motion Correction (MotionCor3)":
        task_motioncor3_handler(project_task, run)
    elif project_task.task.name == 'Assemble stacks (newstack)':
        task_newstack_handler(project_task, run)
    elif project_task.task.name == 'Tomogram Generation (AreTomo)':
        task_aretomo_handler(project_task, run)
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
    parameters = json.loads(project_task.parameter_values)
    project_folder = os.path.join( project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id) )

    task_gain = TaskGain(project_folder)
    task_gain.parameters['input_file'] = parameters[0]
    task_gain.run()
    
    result = task_gain.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()

def task_motioncor2_handler(project_task, run):
    project = project_task.project
    parameter_values = json.loads(project_task.parameter_values)
    project_folder = os.path.join(project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id))
    task_motioncor2 = TaskMotionCor2(project_folder)
    for idx, key in enumerate(TaskMotionCor2.parameter_keys):
        task_motioncor2.parameters[key] = parameter_values[idx]

    task_motioncor2.run()
    
    result = task_motioncor2.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()

def task_motioncor3_handler(project_task, run):
    project = project_task.project
    parameter_values = json.loads(project_task.parameter_values)
    project_folder = os.path.join(project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id))
    task_motioncor3 = TaskMotionCor3(project_folder)
    for idx, key in enumerate(TaskMotionCor3.parameter_keys):
        task_motioncor3.parameters[key] = parameter_values[idx]

    task_motioncor3.run()
    
    result = task_motioncor3.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()

def task_newstack_handler(project_task, run):
    project = project_task.project
    parameter_values = json.loads(project_task.parameter_values)
    project_folder = os.path.join(project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id))
    task_generate_stack = TaskGenerateStack(project_folder)
    for idx, key in enumerate(TaskGenerateStack.parameter_keys):
        task_generate_stack.parameters[key] = parameter_values[idx]

    task_generate_stack.run()
    
    result = task_generate_stack.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()

def task_aretomo_handler(project_task, run):
    project = project_task.project
    parameter_values = json.loads(project_task.parameter_values)
    project_folder = os.path.join(project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id))
    task_aretomo = TaskAreTomo(project_folder)
    for idx, key in enumerate(TaskGenerateStack.parameter_keys):
        task_aretomo.parameters[key] = parameter_values[idx]

    task_aretomo.run()
    
    result = task_aretomo.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()

def task_import_handler(project_task, run):
    project = project_task.project
    parameter_values = json.loads(project_task.parameter_values)
    project_folder = os.path.join(project.folder_path, CONSTANTS.TASK_FOLDER_PREFIX + str(project_task.id))
    task_import = TaskImport(project_folder)
    for idx, key in enumerate(TaskImport.parameter_keys):
        task_import.parameters[key] = parameter_values[idx]

    task_import.run()
    
    result = task_import.get_result()
    run.status = result.status
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    run.logs = json.dumps(result.logs)
    run.errors = json.dumps(result.errors)
    run.output_files = json.dumps(result.output_files)
    run.save()
