from telebot.handler_backends import StatesGroup, State


class StateRecruitment(StatesGroup):
    type_recruitment = State()
    nationality = State()
    university = State()
    birthdate = State()
    surname = State()
    name = State()
    patronymic = State()
    military_station = State()
    field_study = State()
    average_score = State()
    find_out = State()
