from sqlalchemy.orm import Mapped, mapped_column

from app.domain.candidate import Candidate
from .base import BaseModel


class CandidateStorage(BaseModel):
    __tablename__ = 'candidate'
    # TODO: заменить на UUID или ULID
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=True,
        unique=True,
        autoincrement=True,
    )
    user_id: Mapped[str]
    type_recruitment: Mapped[str]
    nationality: Mapped[str]
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str]
    # TODO: заменить на дату после переезда с SQLite
    birthdate: Mapped[str]
    military_station: Mapped[str]
    university: Mapped[str]
    field_study: Mapped[str]
    average_score: Mapped[str]
    find_out: Mapped[str]
    # TODO: добавить уникальность на номер для того, чтоб предотвратить
    # повторное добавление данных в БД.
    phone_number: Mapped[str]

    def into(self) -> Candidate:
        return Candidate(
            user_id=int(self.user_id),
            type_recruitment=self.type_recruitment,
            nationality=self.nationality,
            surname=self.surname,
            name=self.name,
            patronymic=self.patronymic,
            birthdate=self.birthdate,
            military_station=self.military_station,
            university=self.university,
            field_study=self.field_study,
            average_score=self.average_score,
            find_out=self.find_out,
            phone_number=self.phone_number
        )
