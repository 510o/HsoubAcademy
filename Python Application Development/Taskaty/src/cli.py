from .commands import add_task, list_tasks, check_task, remove_task
from argparse import ArgumentParser
from functools import partial
from datetime import date

def build_parser(store):
    parser = ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add the given task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", default=None, type=str, help="Task description")
    add_parser.add_argument("-s", "--start-date", default=None, type=date.fromisoformat, help="Task start date (YYYY-MM-DD)")
    add_parser.add_argument("-e", "--end-date", default=None, type=date.fromisoformat, help="Task end date (YYYY-MM-DD)")
    add_parser.add_argument("--done", action="store_true", help="Mark the task as completed")
    add_parser.set_defaults(func=partial(add_task, store=store, parser=add_parser))

    list_parser = subparsers.add_parser("list", help="List the uncompleted tasks")
    list_parser.add_argument("-a", "--all", help="List all the tasks", action="store_true")
    list_parser.set_defaults(func=partial(list_tasks, store=store))

    check_parser = subparsers.add_parser("check", help="Check the given task")
    check_parser.add_argument("task", type=int, help="Task number to check")
    check_parser.set_defaults(func=partial(check_task, store=store, parser=check_parser))

    remove_parser = subparsers.add_parser("remove", help="Remove the given task")
    remove_parser.add_argument("task", nargs="?", type=int, help="Task number to remove")
    remove_parser.add_argument("-d", "--done", action="store_true", help="Remove completed tasks only")
    remove_parser.add_argument("-a", "--all", action="store_true", help="Remove all tasks")
    remove_parser.set_defaults(func=partial(remove_task, store=store, parser=remove_parser))

    return parser