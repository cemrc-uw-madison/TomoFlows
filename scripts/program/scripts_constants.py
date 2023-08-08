"""
Contents inside data.json
PROJECT_NUM: numbers of projects inside /data 
PROJECTS: (project_name: project_absolute_path) key-value pairs
"""


PROJECT_NUM = "project_num"
PROJECTS = "projects"

"""
Contents inside project.json
TASK_NUM: numbers of tasks inside current project
PROJECT_ID: an project_name + project owner's email + project first created time string
TASKS: (task_name: task_absolute_path) key-value pairs 
"""
TASK_NUM = "task_num"
PROJECT_ID = "project_id"
TASKS = "tasks"
PROJECT_NAME = "project_name"
OWNER = "owner"
CREATED_AT = "created_at"
TASK_FOLDER_PREFIX = "task_"

# CREATED, RUNNING, SUCCESS, FAILED
TASK_STATUS_CREATED = "CREATED"
TASK_STATUS_SUCCESS =  "SUCCESS"
TASK_STATUS_RUNNING = "RUNNING"
TASK_STATUS_FAILED = "FAILED"

"""
Contents inside task folder
"""
TASK_JSON = "task.json"
RESULT_JSON = "result.json"
DATA_SUBFOLDER = "data"

"""
Imageset metadata: descriptions of groupings of data files
"""
IMAGESET_JSON = "imageset.json"
HEADER_IMAGESET_NAME = "imageset_name"

"""
Workflow JSON: a metadata file that supports 'run_process_tilts.py', a headless run.
"""
WORKFLOW_JSON = "workflow.json"