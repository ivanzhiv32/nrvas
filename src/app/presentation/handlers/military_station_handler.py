from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers import (
    UniversityHandler,
)
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class MilitaryStationHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'military_station',
            message.text,
            StateRecruitment.military_station
        )
        bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')
        self.next_handler(message, bot, UniversityHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
