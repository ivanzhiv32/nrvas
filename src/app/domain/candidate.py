from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class Candidate:
    user_id: int
    type_recruitment: str
    nationality: str
    surname: str
    name: str
    patronymic: str
    birthdate: str
    military_station: str
    university: str
    field_study: str
    average_score: str
    find_out: str
    phone_number: str
