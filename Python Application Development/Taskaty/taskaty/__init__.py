"""Taskaty - a simple CLI task manager"""
__version__ = "1.1.0"

from .cli import build_parser
from .storage import load_tasks, save_tasks


def main(argv=None) -> int:
    store = load_tasks()
    parser = build_parser(store)
    args = parser.parse_args(argv)
    code = args.func(args)
    save_tasks(store)
    return code