from dataclasses import dataclass, field


@dataclass(kw_only=True, slots=True)
class Question:
    id: int | None = field(default=None)
    user_id: str
    question: str
    is_answer: bool = field(default=False)
