from abc import abstractmethod, ABC
from pathlib import Path

from app.application.commands.start import StartCommand


class InteractorFactory(ABC):
    @property
    @abstractmethod
    def path(self) -> Path: ...

    @abstractmethod
    def start(self) -> StartCommand: ...
