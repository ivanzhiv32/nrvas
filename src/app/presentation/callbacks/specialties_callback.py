from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.presentation.buttons import get_main_keyboard
from app.presentation.callbacks.base import ICallback


class SpecialtiesCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        path = self.ioc.path

        with open(path / r'documents/Специальности.pdf', 'rb') as file:
            bot.send_document(chat_id, file)
