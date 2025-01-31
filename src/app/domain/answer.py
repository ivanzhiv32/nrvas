from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Answer:
    id: int | None = field(default=None)
    question_id: int
    answer: str
