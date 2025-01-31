from abc import abstractmethod
from typing import Protocol


class ITransaction(Protocol):
    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
