from json import load, dump, JSONDecodeError
from pathlib import Path
from .task import Task
import os


TASKS_FILE = Path.home() / ".taskaty" / "tasks.json"


def load_tasks() -> list[Task]:
    tmp_path = TASKS_FILE.parent / f".{TASKS_FILE.stem}.tmp"
    tmp_path.unlink(missing_ok=True)

    try:
        with open(TASKS_FILE, encoding="utf-8") as f:
            return [Task.from_dict(d) for d in load(f)]
    except FileNotFoundError: return []
    except JSONDecodeError:
        raise SystemExit(f"error: {TASKS_FILE} is corrupted (invalid JSON)")
    except KeyError as e:
        raise SystemExit(f"error: {TASKS_FILE} has malformed task: missing {e}")


def save_tasks(tasks: list[Task]) -> None:
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = TASKS_FILE.parent / f".{TASKS_FILE.stem}.tmp"

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp_path, TASKS_FILE)

    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise