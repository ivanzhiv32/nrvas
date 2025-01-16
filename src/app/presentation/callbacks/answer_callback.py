import json

from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.callbacks.base import ICallback
from app.presentation.handlers.answer_handler import AnswerHandler
from app.utils import excel_to_2d_array


class AnswerCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(req=call.data.split('_')[0])
        df = excel_to_2d_array(self.ioc.path / 'documents/questions.xlsx')
        page = data['NumberPage']

        question = df[4][page]
        bot.send_message(
            call.message.chat.id,
            f'Отправьте ответ на вопрос:\n{question}'
        )
        bot.register_next_step_handler(
            call.message,
            AnswerHandler(self.ioc, question),
        )
