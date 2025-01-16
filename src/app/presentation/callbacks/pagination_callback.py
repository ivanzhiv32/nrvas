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


class PaginateCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.load(call.data.split('_')[0])

        df = excel_to_2d_array(self.ioc.path / 'documents/faq.xlsx')

        questions = len(df) - 1
        pages = questions // 4
        if questions % 4 != 0:
            pages += 1

        bot.edit_message_text(
            text='<b>Выберите интересующий вас вопрос:</b>',
            parse_mode='HTML',
            reply_markup=self._add_keyboard(df, data, pages, questions),
            message_id=call.message.message_id,
        )

    def _add_keyboard(
            self,
            df: DataFrame,
            data: dict[str, Any],
            pages: int,
            questions: int,
    ) -> InlineKeyboardMarkup:
        page = data['NumberPage']
        index = data['IndexQuestion']
        end_index = index + 1
        markup = InlineKeyboardMarkup()
        while index <= end_index and index <= questions:
            question = df[1][index]
            answer = df[2][index]
            markup.add(
                InlineKeyboardButton(
                    text=question,
                    callback_data=f'{{"method":"question","index":"{index}"}}'
                )
            )
            index += 1
        markup.add(
            InlineKeyboardButton(text='Скрыть', callback_data='unseen')
        )
        if page == 1:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method":"pagination","NumberPage":"{page + 1}","IndexQuestion":"{index}"}}',
                ),
            )
        elif page == pages:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{\"method\":\"pagination\",\"NumberPage\":"{page - 1}",\"IndexQuestion\":"{index - 6}"}}'
                ),
                InlineKeyboardButton(
                    text=f'{page}/{pages}',
                    callback_data=' '
                )
            )
        return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method":"pagination","NumberPage":"{page - 1}","IndexQuestion":"{index - 8}"}}'
                ),
                InlineKeyboardButton(
                    text=f'{page}/{pages}',
                    callback_data=' '
                ),
                InlineKeyboardButton(
                    text='Вперёд --->',
                    callback_data=f'{{"method":"pagination","NumberPage":"{page + 1}","IndexQuestion":"{index}"}}'
                )
            )
