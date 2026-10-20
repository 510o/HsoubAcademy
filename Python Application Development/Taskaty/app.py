from src.storage import load_tasks #, save_tasks
from src.cli import build_parser

TASKS_FILE = "tasks.json"

def main(argv=None):
    store = load_tasks(TASKS_FILE)

    parser = build_parser()
    args = parser.parse_args(argv)
    code = args.func(args)

    # save_tasks(TASKS_FILE, store)
    return code


if __name__ == "__main__":
    raise SystemExit(main())