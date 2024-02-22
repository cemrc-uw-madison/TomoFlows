import json

class TaskDescription:
    def __init__(self, task_name, task_description):
        self.task_name = task_name
        self.task_description = task_description
        self.parameters = {}

    def add_parameter(self, name, value):
        self.parameters[name] = value

    def add_parameters(self, dict):
        for key, value in dict.items():
            self.parameters[key] = value

    def save_to_json(self, filename):
        data = {
            'task_name': self.task_name,
            'task_description': self.task_description,
            'parameters': self.parameters
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)

        task_name = data['task_name']
        task_description = data['task_description']
        parameters = data['parameters']

        task = cls(task_name, task_description)
        task.parameters = parameters

        return task

class TaskOutputDescription:
    def __init__(self, task_name, task_description):
        self.task_name = task_name
        self.task_description = task_description
        self.output_files = []
        self.logs = []
        self.errors = []
        self.status = ""

    def add_output_file(self, file_name, file_type):
        self.output_files.append({"file_name": file_name, "file_type": file_type})

    def add_log_file(self, log_name):
        self.logs.append(log_name)
        
    def add_errors(self, error):
        self.errors.append(error)

    def set_status(self, status):
        self.status = status

    def save_to_json(self, filename):
        data = {
            "task_name": self.task_name,
            "task_description": self.task_description,
            "output_files": self.output_files,
            "logs": self.logs,
            "errors": self.errors,
            "status": self.status
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        task_name = data["task_name"]
        task_description = data["task_description"]
        output_files = data["output_files"]
        logs = data["logs"]
        errors = data["errors"]
        status = data["status"]

        task_output = cls(task_name, task_description)
        task_output.output_files = output_files
        task_output.logs = logs
        task_output.errors = errors
        task_output.status = status

        return task_output
