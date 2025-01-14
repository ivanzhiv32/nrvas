from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler


class IDHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(message.chat.id, text=str(message.from_user.id))
