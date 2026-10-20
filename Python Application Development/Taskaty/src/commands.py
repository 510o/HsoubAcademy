from datetime import date
from .task import Task


def add_task(args, store: list[Task]) -> int:
    start_date = args.start_date or date.today()
    end_date = args.end_date
    if args.done and end_date is None:
        end_date = start_date
        
    store.append(Task(
        title=args.title,
        description=args.description,
        start_date=start_date,
        end_date=end_date,
        done=args.done,
    ))
    
    return 0


def list_tasks(args, store: list[Task]) -> int:
    return 0


def check_task(args, store: list[Task]) -> int:
    return 0


def remove_task(args, store: list[Task]) -> int:
    return 0