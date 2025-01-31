from abc import abstractmethod, ABC
from pathlib import Path

from app.application.usecase.answer import AnswerUseCase
from app.application.usecase.candidate import CandidateUseCase
from app.application.usecase.faq import FAQUseCase
from app.application.usecase.question import QuestionUseCase
from app.application.usecase.start import StartUseCase
from app.application.usecase.telegram import TelegramUseCase


class InteractorFactory(ABC):
    @property
    @abstractmethod
    def id_admin(self) -> int: ...

    @property
    @abstractmethod
    def path(self) -> Path: ...

    @abstractmethod
    def start_usecase(self) -> StartUseCase: ...

    @abstractmethod
    def telegram_usecase(self) -> TelegramUseCase: ...

    @abstractmethod
    def faq_usecase(self) -> FAQUseCase: ...

    @abstractmethod
    def candidate_usecase(self) -> CandidateUseCase: ...

    @abstractmethod
    def question_usecase(self) -> QuestionUseCase: ...

    @abstractmethod
    def answer_usecase(self) -> AnswerUseCase: ...
