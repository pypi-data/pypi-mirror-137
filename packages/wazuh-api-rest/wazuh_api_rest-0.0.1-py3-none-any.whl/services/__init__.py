import json

def open_file(file_path) -> [dict]:
    with open(file_path) as tasks_file:
        tasks = json.load(tasks_file)
    return tasks