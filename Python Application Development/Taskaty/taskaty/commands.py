from datetime import date
from .task import Task


def add_task(args, store: list[Task], parser) -> int:
    start_date = args.start_date or date.today()
    end_date = args.end_date
    if args.done and end_date is None:
        end_date = start_date

    if end_date and end_date < start_date:
        parser.error(
            f"argument -e/--end-date: '{end_date}' cannot be earlier than "
            f"argument -s/--start-date: '{start_date}'"
        )
    
    store.append(Task(
        title=args.title,
        description=args.description,
        start_date=start_date,
        end_date=end_date,
        done=args.done,
    ))
    
    return 0


def list_tasks(args, store: list[Task]) -> int:
    if not store:
        print("No tasks yet. Use 'add <title>' to create one")
        return 0

    visible = store if args.all else [t for t in store if not t.done]
    if not visible:
        print("All tasks are checked! Use -a/--all to see them")
        return 0

    dash = "-" if args.ascii else "—"
    check = "[x]" if args.ascii else "✔"
    cross = "[ ]" if args.ascii else "✘"

    header = ["#", "Title", "Description", "Start Date", "End Date"]
    header.append("Done" if args.all else "Due In")

    rows = []
    for i, t in enumerate(store, 1):
        if not args.all and t.done:
            continue
        
        row = [
            str(i),
            t.title,
            t.description or dash,
            t.start_date.isoformat() if t.start_date else dash,
            t.end_date.isoformat() if t.end_date else dash,
            (check if t.done else cross) if args.all else t.due_in()
        ]
        rows.append(row)

    widths = [max(len(str(c)) for c in col) for col in zip(header, *rows)]

    def fmt(r):
        return " | ".join(f"{c:>{w}}" if i == 0 else f"{c:^{w}}" for i, (c, w) in enumerate(zip(r, widths)))

    if args.ascii:
        print(fmt(header))
        print("-+-".join("-" * w for w in widths))
        for row in rows:
            print(fmt(row))
    else:
        def hline(l, m, r): return l + m.join("─" * (w + 2) for w in widths) + r
        def fmt_unicode(r): return "│" + "│".join(f" {c:>{w}} " if i == 0 else f" {c:^{w}} " for i, (c, w) in enumerate(zip(r, widths))) + "│"

        print(hline("┌", "┬", "┐"))
        print(fmt_unicode(header))
        print(hline("├", "┼", "┤"))
        for row in rows:
            print(fmt_unicode(row))
        print(hline("└", "┴", "┘"))
        
    return 0


def _task_index(num: int, store: list[Task], parser) -> int:
    if not store:  parser.error("no tasks available")
    if not (1 <= num <= len(store)):
        parser.error(f"argument task: {num} does not exist (valid: 1..{len(store)})")
    return num - 1


def check_task(args, store: list[Task], parser) -> int:
    idx = _task_index(args.task, store, parser)
    store[idx].done = True
    return 0


def remove_task(args, store: list[Task], parser) -> int:
    flags = [n for n, on in (
        ('<task>',      args.task is not None),
        ('-a/--all',    args.all),
        ('-d/--done',   args.done),
    ) if on]

    if not flags:
        parser.error("specify a task number, -a/--all, or -d/--done")
    if len(flags) > 1:
        parser.error(f"argument {flags[1]}: not allowed with argument {flags[0]}")

    if args.all:
        store.clear()
    elif args.done:
        store[:] = [t for t in store if not t.done]
    else:
        del store[_task_index(args.task, store, parser)]
    return 0