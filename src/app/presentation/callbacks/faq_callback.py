import json
from typing import Any

from pandas import DataFrame
from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.presentation.callbacks.base import ICallback
from app.utils import excel_to_2d_array

COUNT_BUTTONS = 4


class FAQCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        df = excel_to_2d_array(self.ioc.path / 'documents/faq.xlsx')
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text='<b>Выберите интересующий вас вопрос:</b>',
            parse_mode='HTML',
            reply_markup=self._add_keyboard(df, data),
            message_id=call.message.message_id,
        )

    def _add_keyboard(
            self,
            df: DataFrame,
            data: dict[str, Any]
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        page = data['NumberPage']
        count_page = data['CountPages']
        for i in range(COUNT_BUTTONS):
            index = count_page * page + 1 + i
            if index == df[1].count():
                break
            markup.add(
                InlineKeyboardButton(
                    text=df[1][index],
                    callback_data=f'{{"method": "answerFAQ", '
                                  f'"index": {index}}}',
                )
            )
        if page == count_page:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {page - 1}, '
                                  f'"CountPages": {count_page}}}',
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                )
            )
        if page >= 1:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {page - 1}, '
                                  f'"CountPages": {count_page}}}',
                ),
                InlineKeyboardButton(
                    text='Скрыть',
                    callback_data='unseen',
                ),
                InlineKeyboardButton(
                    text='Вперёд --->',
                    callback_data=f'{{"method": "faq", '
                                  f'"NumberPage": {page + 1}, '
                                  f'"CountPages": {count_page}}}'
                )
            )
        return markup.add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen',
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "faq", '
                              f'"NumberPage": {page + 1}, '
                              f'"CountPages": {count_page}}}'
            )
        )


class AnswerFAQCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        df = excel_to_2d_array(self.ioc.path / 'documents/faq.xlsx')
        index = data['index']
        bot.send_message(
            chat_id=call.message.chat.id,
            text=df[2][index]
        )
