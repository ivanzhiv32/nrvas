from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler
from app.presentation.handlers.name_handler import NameHandler
from app.state import StateRecruitment


class SurnameHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'surname',
            message.text,
            StateRecruitment.surname
        )
        bot.send_message(message.from_user.id, 'Напишите Ваше имя')
        self.next_handler(message, bot, NameHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
