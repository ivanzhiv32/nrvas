from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers import AddingQuestionHandler
from app.presentation.handlers.base import IHandler


class QuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot):
        bot.send_message(
            message.from_user.id,
            'Отправьте интересующий Вас вопрос'
        )
        self.next_handler(message, bot, AddingQuestionHandler(self.ioc))
