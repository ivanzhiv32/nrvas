from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.patronymic_handler import PatronymicHandler
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class NameHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'name',
            message.text,
            StateRecruitment.name
        )
        bot.send_message(message.from_user.id, 'Напишите Ваше отчество')
        self.next_handler(message, bot, PatronymicHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
