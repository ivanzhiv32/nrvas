from telebot import TeleBot

from telebot.types import (
    CallbackQuery,
    InputMediaPhoto
)

from app.presentation.callbacks.base import ICallback


class PromoBrochureCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:

        photo1 = open(r'documents/О нас/event_1/Брошюра_page-0001.jpg', 'rb')  # Первое фото
        photo2 = open(r'documents/О нас/event_1/Брошюра_page-0002.jpg', 'rb')  # Второе фото

        media = [
            InputMediaPhoto(photo1),
            InputMediaPhoto(photo2, caption="Брошюра \"О научной роте\"")
        ]

        bot.send_media_group(call.message.chat.id, media)

        photo1.close()
        photo2.close()