from json import load, dump
from pathlib import Path
from .task import Task
import os


def load_tasks(file_name: Path) -> list[Task]:
    tmp_path = file_name.parent / f".{file_name.stem}.tmp"
    tmp_path.unlink(missing_ok=True)

    try:
        with open(file_name, encoding="utf-8") as f:
            return [Task.from_dict(d) for d in load(f)]
    except FileNotFoundError: return []


def save_tasks(file_name: Path, tasks: list[Task]) -> None:
    file_name.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = file_name.parent / f".{file_name.stem}.tmp"

    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
            f.flush(); os.fsync(f.fileno())
        os.replace(tmp_path, file_name)

    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise