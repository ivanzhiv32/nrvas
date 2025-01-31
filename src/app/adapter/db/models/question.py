import datetime as dt

from sqlalchemy.orm import Mapped, mapped_column

from app.domain.question import Question
from .base import BaseModel


class QuestionStorage(BaseModel):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    user_id: Mapped[str]
    question: Mapped[str]
    date_on: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now(),
    )
    is_answer: Mapped[bool]

    def into(self) -> Question:
        return Question(
            id=self.id,
            user_id=self.user_id,
            question=self.question,
            is_answer=self.is_answer,
        )
