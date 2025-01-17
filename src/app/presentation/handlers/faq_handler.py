from pandas import DataFrame
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.presentation.handlers.base import IHandler
from app.utils import excel_to_2d_array

COUNT_BUTTONS = 4


class FAQHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        # TODO: добавить БД
        df = excel_to_2d_array(self.ioc.path / 'documents/faq.xlsx')
        length = df.shape[0] - 1
        bot.send_message(
            message.chat.id,
            text=f'<b>Выберите интересующий вас вопрос</b>',
            parse_mode="HTML",
            reply_markup=self._get_keyboard(df, length)
        )

    def _get_keyboard(self, df: DataFrame, count_page: int):
        markup = InlineKeyboardMarkup()
        page = 0
        for i in range(COUNT_BUTTONS):
            markup.add(
                InlineKeyboardButton(
                    text=df[1][i + 1],
                    callback_data=f'{{"method": "answerFAQ", '
                                  f'"index": {i + 1}}}',
                )
            )
        count_page = count_page // 4 if count_page % 4 != 0 else count_page + 1
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
