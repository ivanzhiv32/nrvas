from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers import AverageScoreHandler
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class FieldStudyHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'field_study',
            message.text,
            StateRecruitment.field_study
        )
        bot.send_message(
            message.from_user.id,
            'Напишите средний балл по диплому (х.х)'
        )
        self.next_handler(message, bot, AverageScoreHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
