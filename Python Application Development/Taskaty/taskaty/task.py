from dataclasses import dataclass, asdict
from datetime import date

@dataclass
class Task:
    title: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    done: bool = False

    def due_in(self, today: date | None = None) -> str:
        today = today or date.today()

        if self.end_date is None: return "Open"
        if self.done: return "Done"

        delta = (self.end_date - today).days
        if delta < 0: return f"{-delta}d overdue"
        if delta == 0: return "Today"
        if delta == 1: return "Tomorrow"
        return f"in {delta}d"

    def to_dict(self) -> dict:
        d = asdict(self)
        for key in ("start_date", "end_date"):
            if d[key] is not None: d[key] = d[key].isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        def parse(v):
            return date.fromisoformat(v) if v else None
        
        return cls(
            title=d["title"],
            description=d.get("description"),
            start_date=parse(d.get("start_date")),
            end_date=parse(d.get("end_date")),
            done=d.get("done", False)
        )

    def to_list(self) -> list[str]:
        return [
            self.title,
            self.description or "—",
            self.start_date.isoformat() if self.start_date else "—",
            self.end_date.isoformat() if self.end_date else "—",
        ]