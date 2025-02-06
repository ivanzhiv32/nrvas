from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.domain.question import Question


class IQuestionGateway(Protocol):
    @abstractmethod
    def add(self, source: Question) -> Question: ...

    @abstractmethod
    def update_is_answer(self, source: Question) -> Question: ...

    @abstractmethod
    def get(self, question_id: int) -> Question: ...

    @abstractmethod
    def get_question(self, limit: int, offset: int) -> Question | None: ...

    @abstractmethod
    def get_total(self) -> int: ...
