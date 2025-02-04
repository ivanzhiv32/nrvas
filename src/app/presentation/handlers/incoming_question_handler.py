from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.application.usecase.question import QuestionList
from app.presentation.handlers.base import IHandler

LIMIT = 1


class IncomingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        usecase = self.ioc.question_usecase()
        try:
            model = usecase.get_questions(LIMIT, 0)
            bot.send_message(
                message.chat.id,
                text=f'<b>{model.question.question}</b>',
                parse_mode='HTML',
                reply_markup=self._get_keyboard(model)
            )
        except ValueError:
            bot.send_message(
                message.chat.id,
                text='<b>Пользователи не задали ни одного вопроса</b>',
                parse_mode='HTML',
            )

    def _get_keyboard(self, model: QuestionList) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method": "answer", '
                              f'"index": {model.question.id}}}',
            )
        )
        if model.total < LIMIT:
            return markup.add(
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                ),
            )
        offset = model.offset + 1
        return markup.add(
            InlineKeyboardButton(
                text='➡️',
                callback_data=f'{{"method": "questions", '
                              f'"NumberPage": {offset}}}'
            )
        ).add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen',
            ),
        )
