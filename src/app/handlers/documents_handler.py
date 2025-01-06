from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from app.constants import FEDERAL_ACT, CONSULTANT_URL


def documents_handler(message: Message, bot: TeleBot) -> None:
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        'Ссылка',
        url=CONSULTANT_URL,
    )
    markup.add(button1)

    bot.send_message(message.chat.id,
                     text=FEDERAL_ACT,
                     reply_markup=markup)
