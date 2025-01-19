from collections.abc import Callable, Iterator
from pathlib import Path

from sqlalchemy.orm import Session

from app.adapter.db.gateway.faq import FAQGateway
from app.application.commands.faq_command import FAQCommand
from app.application.commands.start_command import StartCommand
from app.application.commands.telegram_command import TelegramCommand
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            path: Path,
            id_admin,
            transaction: Callable[[], Iterator[Session]]
    ) -> None:
        self._path = path
        self._id_admin = id_admin
        self._transaction = transaction

    @property
    def session(self) -> Session:
        for session in self._transaction():
            return session

    @property
    def id_admin(self) -> int:
        return self._id_admin

    @property
    def path(self) -> Path:
        return self._path

    def faq_command(self) -> FAQCommand:
        session = self.session
        gateway = FAQGateway(session)
        return FAQCommand(gateway, session)

    def start(self) -> StartCommand:
        return StartCommand(path=self.path, id_admin=self.id_admin)

    def telegram(self) -> TelegramCommand:
        return TelegramCommand()
