from sqlalchemy.orm import Mapped, mapped_column

from app.domain.faq import FAQ
from .base import BaseModel


class FAQStorage(BaseModel):
    __tablename__ = 'faq'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    question: Mapped[str]
    answer: Mapped[str]

    def into(self) -> FAQ:
        return FAQ(
            id=self.id,
            question=self.question,
            answer=self.answer
        )
