import json

import json

class WorkflowMetadata:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name, task_parameters):
        task = {
            "name": task_name,
            "parameters": task_parameters
        }
        self.tasks.append(task)

    def save_to_json(self, filename):
        data = {
            "tasks": self.tasks
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        task_list = cls()
        task_list.tasks = data["tasks"]

        return task_list
