from telebot import TeleBot
from telebot.types import Message

from app.constants import TELEGRAM_CHANNEL


def telegram_channel_handler(message: Message, bot: TeleBot) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text=TELEGRAM_CHANNEL,
    )
