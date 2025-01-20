from collections.abc import Iterator
from pathlib import Path

from sqlalchemy.orm import Session

from app.adapter.db.gateway.candidate import CandidateGateway
from app.adapter.db.gateway.faq import FAQGateway
from app.adapter.persistence.db import create_session_maker, get_session
from app.application.usecase.candidate import CandidateUseCase
from app.application.usecase.faq import FAQUseCase
from app.application.usecase.start import StartUseCase
from app.application.usecase.telegram import TelegramUseCase
from app.presentation.interactor import InteractorFactory


class IoC(InteractorFactory):
    def __init__(
            self,
            path: Path,
            id_admin,
            db_url: str
    ) -> None:
        self._path = path
        self._id_admin = id_admin
        self._db_url = db_url

    @property
    def session(self) -> Iterator[Session]:
        session_maker = create_session_maker(self._db_url)
        return get_session(session_maker)

    @property
    def id_admin(self) -> int:
        return self._id_admin

    @property
    def path(self) -> Path:
        return self._path

    def faq_usecase(self) -> FAQUseCase:
        for session in self.session:
            gateway = FAQGateway(session)
            return FAQUseCase(gateway, session)

    def start_usecase(self) -> StartUseCase:
        return StartUseCase(path=self.path, id_admin=self.id_admin)

    def telegram_usecase(self) -> TelegramUseCase:
        return TelegramUseCase()

    def candidate_usecase(self) -> CandidateUseCase:
        for session in self.session:
            gateway = CandidateGateway(session)
            return CandidateUseCase(
                gateway=gateway,
                transaction=session
            )
