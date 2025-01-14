from pandas import DataFrame
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.presentation.handlers.base import IHandler
from app.utils import excel_to_2d_array


class FaqHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        # TODO: добавить БД
        df = excel_to_2d_array(self.ioc.path / 'faq.xlsx')
        page = 1
        length = len(df) - 1

        count = length // 4
        if length % 4 != 0:
            count += 1
        bot.send_message(
            message.chat.id,
            text=f'<b>Выберите интересующий вас вопрос</b>',
            parse_mode="HTML",
            reply_markup=self._get_keyboard(df, count, page)
        )

    def _get_keyboard(self, df: DataFrame, count: int, page: int):
        markup = InlineKeyboardMarkup()
        i = 1
        while i <= 4:
            question = df[1][i]
            markup.add(
                InlineKeyboardButton(
                    text=question,
                    callback_data=f'{{"method":"question", "index": {i}}}',
                )
            )
            i += 1
        return markup.add(
            InlineKeyboardButton(
                text='Скрыть',
                callback_data='unseen'
            )
        ).add(
            InlineKeyboardButton(
                text=f'{page}/{count}',
                callback_data=' '
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method": "question", '
                              f'"NumberPage": {page + 1}, '
                              f'"IndexQuestion": {i}}}'
            )
        )
