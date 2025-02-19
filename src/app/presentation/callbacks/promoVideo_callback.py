from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.presentation.buttons import get_main_keyboard
from app.presentation.callbacks.base import ICallback


class PromoVideoCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        path = self.ioc.path

        with open(path / r'documents/Промо ролик.mp4', 'rb') as file:
            bot.send_video(chat_id, file, timeout=600)

        file.close()