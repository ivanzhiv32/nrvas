from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.military_station_handler import MilitaryStationHandler
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class PatronymicHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'patronymic',
            message.text,
            StateRecruitment.patronymic
        )
        bot.send_message(
            message.from_user.id,
            'Напишите название своего военного комиссариата'
        )
        self.next_handler(
            message,
            bot,
            MilitaryStationHandler(self.ioc)
        )
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
