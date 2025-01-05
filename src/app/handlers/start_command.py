from pathlib import Path

from telebot import TeleBot
from telebot.types import Message

from app.buttons import get_keyboard
from app.constants import WELCOME_MESSAGE
from app.utils import check_is_admin


class StartCommand:
    def __init__(
            self,
            bot: TeleBot,
            dir_sticker: Path,
            id_admin: int
    ) -> None:
        self.bot = bot
        self.dir_sticker = dir_sticker
        self.id_admin = id_admin

    def __call__(self, message: Message) -> None:
        with open(self.dir_sticker, 'rb') as file:
            self.bot.send_sticker(message.chat.id, file)

        if message.from_user.last_name is None:
            welcome_name = f'{message.from_user.first_name}'
        else:
            welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
        is_admin = check_is_admin(
            message=message,
            id_admin=self.id_admin,
        )
        self.bot.send_message(
            message.chat.id,
            WELCOME_MESSAGE.format(welcome_name=welcome_name),
            parse_mode='html',
            reply_markup=get_keyboard(is_admin),
        )
