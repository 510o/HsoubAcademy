from .commands import add_task, list_tasks, check_task, remove_task
from argparse import ArgumentParser
from functools import partial # lambda
from datetime import date

def build_parser(store):
    parser = ArgumentParser(description='Simple CLI Task Manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Add the given task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('-d', '--description', help='Task description', type=str, default=None)
    add_parser.add_argument('-s', '--start-date', help='Task start date (YYYY-MM-DD)', type=date.fromisoformat, default=None)
    add_parser.add_argument('-e', '--end-date', help='Task end date (YYYY-MM-DD)', type=date.fromisoformat, default=None)
    add_parser.add_argument('--done', help='Mark the task as completed', action='store_true')
    add_parser.set_defaults(func=partial(add_task, store=store))

    list_parser = subparsers.add_parser('list', help='List the uncompleted tasks')
    list_parser.add_argument('-a', '--all', help='List all the tasks', action='store_true')
    list_parser.set_defaults(func=partial(list_tasks, store=store))

    check_parser = subparsers.add_parser('check', help='Check the given task')
    check_parser.add_argument('-t', '--task', help='Number of the task to be completed. If not specified, last task will be completed', type=int)
    check_parser.set_defaults(func=partial(check_task, store=store))

    remove_parser = subparsers.add_parser('remove', help='Remove the given task')
    remove_parser.add_argument('-t', '--task', help='Number of the task to be removed', type=int)
    remove_parser.add_argument('-a', '--all', help='Remove all tasks', action='store_true')
    remove_parser.set_defaults(func=partial(remove_task, store=store))

    return parser