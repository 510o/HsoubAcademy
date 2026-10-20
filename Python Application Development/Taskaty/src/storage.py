from json import load, dump
from .task import Task

def load_tasks(file_name: str) -> list[Task]:
    try:
        with open(file_name, encoding='utf-8') as f:
            return [Task.from_dict(d) for d in load(f)]
    except FileNotFoundError:
        return []

