from telebot import TeleBot
from telebot.types import Message


def id_handler(message: Message, bot: TeleBot) -> None:
    user_id = message.from_user.id
    bot.send_message(message.chat.id, text=f'{user_id}')
