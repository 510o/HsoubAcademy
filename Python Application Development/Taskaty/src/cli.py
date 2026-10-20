from .commands import add_task, list_tasks, check_task, remove_task
from argparse import ArgumentParser

def build_parser():
    parser = ArgumentParser(description='Simple CLI Task Manager')
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser('add', help='Add the given task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('-d', '--description', help='Task description', type=str, default=None)
    add_parser.add_argument('-s', '--start-date', help='Task start date', type=str, default=None)
    add_parser.add_argument('-e', '--end-date', help='Task end date', type=str, default=None)
    add_parser.add_argument('--done', help='Mark the task as completed', action='store_true')
    add_parser.set_defaults(func=add_task)

    list_parser = subparsers.add_parser('list', help='List the uncompleted tasks')
    list_parser.add_argument('-a', '--all', help='List all the tasks', action='store_true')
    list_parser.set_defaults(func=list_tasks)

    check_parser = subparsers.add_parser('check', help='Check the given task')
    check_parser.add_argument('-t', '--task', help='Number of the task to be completed. If not specified, last task will be completed', type=int)
    check_parser.set_defaults(func=check_task)

    remove_parser = subparsers.add_parser('remove', help='Remove the given task')
    remove_parser.add_argument('-t', '--task', help='Number of the task to be removed', type=int)
    remove_parser.add_argument('-a', '--all', help='Remove all tasks', action='store_true')
    remove_parser.set_defaults(func=remove_task)

    return parser