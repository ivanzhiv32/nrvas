from telebot import TeleBot
from telebot.types import Message

from app.presentation.buttons import get_type_recruitment_keyboard


def type_recruitment_handler(message: Message, bot: TeleBot) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text='На какой призыв Вы хотите оставить заявку?',
        reply_markup=get_type_recruitment_keyboard(),
    )
