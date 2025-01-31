from dataclasses import dataclass


@dataclass()
class FAQ:
    id: int
    question: str
    answer: str
