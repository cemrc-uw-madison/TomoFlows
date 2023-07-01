import json
import time
import random
import pytz
import os
from datetime import datetime
from scripts.program.task_gain import TaskGain
from django.conf import settings

def task_handler(project_task, run):
    if project_task.task.name == "Gain":
        task_gain_handler(project_task, run)
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
    logs = []
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Running Gain task...",
    })
    task_gain = TaskGain(os.path.join(settings.BASE_DIR, "scripts/tests/TestData/Gain/test1"), "input.dm4")
    task_gain.run()
    run.status = "SUCCESS"
    run.end_time = datetime.now().replace(tzinfo=pytz.utc)
    logs.append({
        "timestamp": str(datetime.now().replace(tzinfo=pytz.utc)),
        "detail": "Gain task run completed successfully"
    })
    run.logs = json.dumps(logs)
    run.errors = json.dumps([])
    run.save()

