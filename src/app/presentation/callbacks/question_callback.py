import json
from typing import Any

from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from app.application.usecase.question import QuestionList
from app.presentation.callbacks.base import ICallback

LIMIT = 1


class QuestionsCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        usecase = self.ioc.question_usecase()
        offset = data['NumberPage']
        model = usecase.get_questions(LIMIT, offset)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=f'<b>{model.question.question}</b>',
            parse_mode='HTML',
            reply_markup=self._get_keyboard(model, data),
            message_id=call.message.message_id,
        )

    def _get_keyboard(
            self,
            model: QuestionList,
            data: dict[str, Any]
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method": "answer", '
                              f'"index": {model.question.id}}}',
            )
        )
        offset = data['NumberPage']
        if offset + 1 == model.total:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "questions", '
                                  f'"NumberPage": {offset - 1}}}'
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                )
            )
        elif offset > 0:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "questions", '
                                  f'"NumberPage": {offset - 1}}}'
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                ),
                InlineKeyboardButton(
                    text='Вперёд --->',
                    callback_data=f'{{"method": "questions", '
                                  f'"NumberPage": {offset + 1}}}'
                )
            )
        return markup.add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen',
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "questions", '
                              f'"NumberPage": {offset + 1}}}'
            )
        )
