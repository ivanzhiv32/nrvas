import json

from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.callbacks.base import ICallback
from app.presentation.handlers.answer_handler import AnswerToQuestionHandler


class AnswerCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        usecase = self.ioc.question_usecase()
        data = json.loads(call.data)
        question_id = data['index']
        question = usecase.get(question_id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Пользователь задал вопрос:\n\n<b>{question.question}</b>\n\n'
                 'Напишите ему ответ:'
        )
        self.next_handler(
            call.message,
            bot,
            AnswerToQuestionHandler(self.ioc, int(question_id))
        )
