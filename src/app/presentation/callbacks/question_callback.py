import json
from typing import Any

from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.presentation.callbacks.base import ICallback
from app.utils import excel_to_2d_array


class QuestionCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        data = json.loads(call.data)
        df = excel_to_2d_array(self.ioc.path / 'documents/questions.xlsx')
        page = data['NumberPage']
        question = df[3][page]
        pages = len(df) - 1
        bot.edit_message_text(
            text=question,
            parse_mode='HTML',
            reply_markup=self._get_keyboard(page, pages),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )

    def _get_keyboard(self, page: int, pages: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method":"answer","NumberPage":"{page}"}}'
            )
        )
        if page == 1:
            return markup.add(
                InlineKeyboardButton(
                    text=f'{page}/{pages}',
                    callback_data='  '
                ),
                InlineKeyboardButton(
                    text='Вперёд --->',
                    callback_data=f'{{"method":"question","NumberPage":"{page + 1}"'
                                  f',"IndexQuestion":"{page}"}}'
                )
            )
        elif page == pages:
            return markup.add(
                InlineKeyboardButton(
                    text='<--- Назад',
                    callback_data=f'{{"method":"question","NumberPage":"{page - 1}"'
                                  f',"IndexQuestion":"{page - 1}"}}'
                ),
                InlineKeyboardButton(
                    text=f'{page}/{pages}',
                    callback_data=' '
                )
            )
        return markup.add(
            InlineKeyboardButton(
                text='<--- Назад',
                callback_data=f'{{"method":"question","NumberPage":"{page - 1}",'
                              f'"IndexQuestion":"{page + -1}"}}'
            ),
            InlineKeyboardButton(
                text=f'{page}/{pages}',
                callback_data=' '
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method":"question","NumberPage":"{page + 1}",'
                              f'"IndexQuestion":"{page + 1}"}}'
            )
        )
