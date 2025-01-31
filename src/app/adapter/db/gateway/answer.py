from sqlalchemy import insert

from app.adapter.db.models import AnswerStorage
from app.domain.answer import Answer
from .base import BaseGateway


class AnswerGateway(BaseGateway[Answer]):
    def add(self, source: Answer) -> Answer:
        stmt = insert(AnswerStorage).values(
            question_id=source.question_id,
            answer=source.answer
        ).returning(AnswerStorage)
        result = self.session.execute(stmt)
        return result.scalar().into()
