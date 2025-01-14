from abc import abstractmethod, ABC
from pathlib import Path

from app.application.commands.start_command import StartCommand
from app.application.commands.telegram_command import TelegramCommand


class InteractorFactory(ABC):
    @property
    @abstractmethod
    def path(self) -> Path: ...

    @abstractmethod
    def start(self) -> StartCommand: ...

    @abstractmethod
    def telegram(self) -> TelegramCommand: ...
