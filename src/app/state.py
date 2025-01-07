from telebot.handler_backends import StatesGroup, State


class StateRecruitment(StatesGroup):
    type_recruitment = State()
    nationality = State()
