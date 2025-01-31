from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler


class AboutHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            text='<b>Данная кнопка находится в разработке</b>',
            parse_mode='HTML'
        )
