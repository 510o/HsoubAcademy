from dataclasses import dataclass, asdict
from datetime import date

@dataclass
class Task:
    title: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    done: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        for key in ("start_date", "end_date"):
            if d[key] is not None: d[key] = d[key].isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Task:
        def parse(v):
            return date.fromisoformat(v) if v else None
        
        return cls(
            title=d["title"],
            description=d.get("description"),
            start_date=parse(d.get("start_date")),
            end_date=parse(d.get("end_date")),
            done=d.get("done", False)
        )