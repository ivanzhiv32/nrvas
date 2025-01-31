from sqlalchemy import insert

from app.adapter.db.models import CandidateStorage
from app.domain.candidate import Candidate
from .base import BaseGateway


class CandidateGateway(BaseGateway[Candidate]):
    def add(self, candidate: Candidate) -> Candidate:
        # TODO: user_id должен быть один, исправить в дальнейшем
        stmt = insert(CandidateStorage).values(
            user_id=str(candidate.user_id),
            type_recruitment=candidate.type_recruitment,
            nationality=candidate.nationality,
            surname=candidate.surname,
            name=candidate.name,
            patronymic=candidate.patronymic,
            birthdate=candidate.birthdate,
            military_station=candidate.military_station,
            university=candidate.university,
            field_study=candidate.field_study,
            average_score=candidate.average_score,
            find_out=candidate.find_out,
            phone_number=candidate.phone_number,
        ).returning(CandidateStorage)
        result = self.session.execute(stmt)
        return result.scalar().into()
