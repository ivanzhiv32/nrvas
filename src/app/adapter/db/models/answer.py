import datetime as dt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.answer import Answer
from .base import BaseModel


class AnswerStorage(BaseModel):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    answer: Mapped[str]
    date_on: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now(),
    )

    def into(self) -> Answer:
        return Answer(
            id=self.id,
            question_id=self.question_id,
            answer=self.answer,
        )
