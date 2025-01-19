import uuid
from collections.abc import Iterator

from sqlalchemy import select, func

from app.adapter.db.models.faq import FAQStorage
from .base import BaseGateway


class FAQGateway[FAQ](BaseGateway):
    def get_all(self, limit: int, offset: int) -> Iterator[FAQ]:
        stmt = select(FAQStorage).limit(limit).offset(offset)
        result = self.session.execute(stmt)
        return (model.into() for model in result.scalars())

    def total(self) -> int:
        stmt = select(
            func.count(FAQStorage.id)
        )
        result = self.session.scalar(stmt)
        return result

    def get(self, id: int) -> FAQ | None:
        stmt = select(FAQStorage).where(FAQStorage.id == id)
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is not None:
            return model.into()
        return model
