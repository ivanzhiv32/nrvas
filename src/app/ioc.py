from pathlib import Path

from app.application.commands.start import StartCommand
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(self, path: Path, id_admin) -> None:
        self._path = path
        self.id_admin = id_admin

    @property
    def path(self) -> Path:
        return self._path

    def start(self) -> StartCommand:
        return StartCommand(path=self.path, id_admin=self.id_admin)
