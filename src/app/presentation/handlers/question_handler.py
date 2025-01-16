from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers import AddingQuestionHandler
from app.presentation.handlers.base import IHandler


class QuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot):
        bot.send_message(
            message.from_user.id,
            'Отправьте интересующий вас вопрос'
        )
        bot.register_next_step_handler(message, AddingQuestionHandler(self.ioc))
