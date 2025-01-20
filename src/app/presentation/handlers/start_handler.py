from telebot import TeleBot
from telebot.types import Message

from app.presentation.buttons import get_main_keyboard
from app.presentation.handlers.base import IHandler


class StartHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        start_command = self.ioc.start_usecase()
        chat_id = message.chat.id
        with open(start_command.file, 'rb') as file:
            bot.send_sticker(chat_id, file)
        user_id = message.from_user.id
        bot.send_message(
            chat_id,
            start_command.get_text(message.from_user.full_name),
            reply_markup=get_main_keyboard(user_id == start_command.id_admin)
        )
