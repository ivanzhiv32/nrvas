from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.field_study_handler import FieldStudyHandler
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class UniversityHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'university',
            message.text,
            StateRecruitment.university
        )
        bot.send_message(
            message.from_user.id,
            'Напишите направление подготовки в ВУЗе'
        )
        self.next_handler(message, bot, FieldStudyHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
