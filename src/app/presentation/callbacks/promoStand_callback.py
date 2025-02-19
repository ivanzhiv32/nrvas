from telebot import TeleBot

from telebot.types import (
    CallbackQuery,
    InputMediaPhoto
)

from app.presentation.callbacks.base import ICallback


class PromoStandCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:

        photo = open(r'documents/О нас/event_3/Стенд_page-0001.jpg', 'rb')

        bot.send_photo(call.message.chat.id, photo, caption="Стенд \"О научной роте\"")

        photo.close()
