from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler


class TelegramChannelHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        # TODO: добавить базу данных, откуда будет браться телеграмм канал
        telegram = self.ioc.telegram_usecase()
        bot.send_message(
            chat_id=message.chat.id,
            text=telegram.channel,
        )
