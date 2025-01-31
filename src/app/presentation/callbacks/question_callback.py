import json
from typing import Any

from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from app.application.usecase.question import QuestionList
from app.presentation.callbacks.base import ICallback

LIMIT = 5


class QuestionsCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        usecase = self.ioc.question_usecase()
        offset = data['NumberPage']
        model = usecase.get_questions(LIMIT, offset)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text='<b>Пользователи задали следующие вопросы</b>',
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
        for _, value in enumerate(model.questions):
            markup.add(
                InlineKeyboardButton(
                    text=value.question,
                    callback_data=f'{{"method": "answer", '
                                  f'"index": {value.id}}}',
                )
            )
        offset = data['NumberPage']
        if len(model.questions) < model.limit or model.questions == 0:
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
