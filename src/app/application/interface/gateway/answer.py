from abc import abstractmethod
from typing import Protocol

from app.domain.answer import Answer


class IAnswerGateway(Protocol):
    @abstractmethod
    def add(self, source: Answer) -> Answer: ...
