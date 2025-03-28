from telebot import TeleBot
from telebot.types import Message

from app.presentation.handlers.base import IHandler
from app.presentation.interactor import InteractorFactory


class AnswerHandler(IHandler):
    def __init__(self, ioc: InteractorFactory, question: str) -> None:
        super().__init__(ioc)
        self.question = question

    def __call__(
            self,
            message: Message,
            bot: TeleBot,
    ) -> None:
        text = (f'<b>Представитель научной роты ответил на Ваш '
                f'вопрос.</b>\n{self.question}\n{message.text}')
        bot.send_message(self.ioc.id_admin, text, parse_mode='HTML')
        bot.send_message(
            message.from_user.id,
            'Ответ на данный вопрос отправлен пользователю'
        )


class AnswerToQuestionHandler(IHandler):
    def __init__(self, ioc: InteractorFactory, question_id: int, user_id: int) -> None:
        super().__init__(ioc)
        self._question_id = question_id
        self._user_id = user_id

    def __call__(self, message: Message, bot: TeleBot) -> None:
        usecase = self.ioc.answer_usecase()
        text = message.text
        usecase.add_answer(self._question_id, text)
        bot.send_message(
            message.from_user.id,
            'Ответ добавлен в базу данных'
        )
        bot.send_message(
            self._user_id,
            f'<b>Ответ представителя на Ваш вопрос:</b>\n\n{text}',
            parse_mode='HTML',
        )
