from abc import abstractmethod
from collections.abc import Iterator
from typing import Protocol

from app.domain.faq import FAQ


class IFAQGateway(Protocol):
    @abstractmethod
    def get_all(self, limit: int, offset: int) -> Iterator[FAQ]: ...

    @abstractmethod
    def total(self) -> int: ...

    @abstractmethod
    def get(self, id: int) -> FAQ | None: ...
