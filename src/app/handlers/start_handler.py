from pathlib import Path

from telebot import TeleBot
from telebot.types import Message

from app.buttons import get_keyboard
from app.constants import WELCOME_MESSAGE


class StartHandler:
    def __init__(
            self,
            dir_sticker: Path,
            id_admin: int
    ) -> None:
        self.dir_sticker = dir_sticker
        self.id_admin = id_admin

    def __call__(self, message: Message, bot: TeleBot) -> None:
        with open(self.dir_sticker, 'rb') as file:
            bot.send_sticker(message.chat.id, file)

        if message.from_user.last_name is None:
            welcome_name = f'{message.from_user.first_name}'
        else:
            welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
        bot.send_message(
            message.chat.id,
            WELCOME_MESSAGE.format(welcome_name=welcome_name),
            parse_mode='html',
            reply_markup=get_keyboard(message.from_user.id == self.id_admin),
        )
