from telebot import TeleBot
from telebot.types import Message

from app.presentation.buttons import get_main_keyboard
from app.presentation.interactor import InteractorFactory


class StartHandler:
    def __init__(
            self,
            ioc: InteractorFactory,
    ) -> None:
        self.ioc = ioc

    def __call__(self, message: Message, bot: TeleBot) -> None:
        start_command = self.ioc.start()
        chat_id = message.chat.id
        with open(start_command.file, 'rb') as file:
            bot.send_sticker(chat_id, file)
        user_id = message.from_user.id
        bot.send_message(
            chat_id,
            start_command.get_text(message.from_user.full_name),
            reply_markup=get_main_keyboard(user_id == start_command.id_admin)
        )
