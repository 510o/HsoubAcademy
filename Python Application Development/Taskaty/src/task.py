from dataclasses import dataclass

@dataclass
class Task:
    title: str
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    done: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> Task:
        return cls(
            title=d["title"],
            description=d.get("description"),
            start_date=d.get("start_date"),
            end_date=d.get("end_date"),
            done=d.get("done", False)
        )