from collections.abc import Iterator

from sqlalchemy import insert, select, update, func

from app.adapter.db.models import QuestionStorage
from app.domain.question import Question
from .base import BaseGateway


class QuestionGateway(BaseGateway[Question]):
    def add(self, source: Question) -> Question:
        stmt = (
            insert(QuestionStorage)
            .values(
                user_id=source.user_id,
                question=source.question,
                is_answer=source.is_answer,
            )
            .returning(QuestionStorage)
        )
        result = self.session.execute(stmt)
        return result.scalar().into()

    def update_is_answer(self, source: Question) -> Question:
        stmt = (
            update(QuestionStorage)
            .values(
                is_answer=source.is_answer
            )
            .where(QuestionStorage.id == source.id)
            .returning(QuestionStorage)
        )
        result = self.session.execute(stmt)
        return result.scalar().into()

    def get(self, question_id: int) -> Question | None:
        stmt = select(QuestionStorage).where(
            QuestionStorage.id == question_id,
        )
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is not None:
            return model.into()
        return model

    def get_all(self, limit: int, offset: int) -> Iterator[Question]:
        stmt = (select(QuestionStorage)
        .limit(limit)
        .offset(offset)
        .where(
            QuestionStorage.is_answer == False
        ))
        result = self.session.execute(stmt)
        return (model.into() for model in result.scalars())

    def get_total(self) -> int:
        stmt = (
            select(func.count(QuestionStorage.id))
            .where(QuestionStorage.is_answer == False)
        )
        result = self.session.scalar(stmt)
        return result
