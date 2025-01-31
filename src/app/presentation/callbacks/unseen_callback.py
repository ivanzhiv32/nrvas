from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.callbacks.base import ICallback


class UnseenCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        bot.delete_message(call.message.chat.id, call.message.message_id)
