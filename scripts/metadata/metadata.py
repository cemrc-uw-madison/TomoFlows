import json

class TaskDescription:
    def __init__(self, task_name, task_description):
        self.task_name = task_name
        self.task_description = task_description
        self.parameters = {}

    def add_parameter(self, name, value):
        self.parameters[name] = value

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

