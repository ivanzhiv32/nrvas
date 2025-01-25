from telebot import TeleBot
from telebot.types import Message

from app.domain.question import Question
from app.presentation.handlers.base import IHandler


class AddingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.from_user.id,
            'Спасибо за вопрос, он добавлен в базу. '
            'В скором времени на него ответят и вам придет уведомление.'
        )
        self._add_question(message.from_user.id, message.text)
        bot.send_message(
            self.ioc.id_admin,
            f'Пользователь (@{message.from_user.username}) задал вопрос'
        )

    def _add_question(self, user_id: int, question: str) -> None:
        question = Question(
            user_id=str(user_id),
            question=question,
        )
        usecase = self.ioc.question_usecase()
        usecase.add_question(question)
