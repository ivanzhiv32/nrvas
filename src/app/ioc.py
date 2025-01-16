from pathlib import Path

from app.application.commands.start_command import StartCommand
from app.application.commands.telegram_command import TelegramCommand
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(self, path: Path, id_admin) -> None:
        self._path = path
        self._id_admin = id_admin

    @property
    def id_admin(self) -> int:
        return self._id_admin

    @property
    def path(self) -> Path:
        return self._path

    def start(self) -> StartCommand:
        return StartCommand(path=self.path, id_admin=self.id_admin)

    def telegram(self) -> TelegramCommand:
        return TelegramCommand()
