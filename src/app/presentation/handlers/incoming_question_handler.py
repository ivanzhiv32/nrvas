from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.application.usecase.question import QuestionList
from app.presentation.handlers.base import IHandler

LIMIT = 5


class IncomingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        usecae = self.ioc.question_usecase()
        model = usecae.get_questions(LIMIT, 0)
        try:
            bot.send_message(
                message.chat.id,
                text='<b>Пользователи задали следующие вопросы</b>',
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
        for _, value in enumerate(model.questions):
            markup.add(
                InlineKeyboardButton(
                    text=value.question,
                    callback_data=f'{{"method": "answer", '
                                  f'"index": {value.id}}}',
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
                text='Скрыть',
                callback_data='unseen',
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "questions", '
                              f'"NumberPage": {offset}}}'
            )
        )
