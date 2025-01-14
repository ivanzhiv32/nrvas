from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.presentation.handlers.base import IHandler
from app.utils import excel_to_2d_array


class IncomingQuestionHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        # TODO: добавить БД
        df = excel_to_2d_array(self.ioc.path / 'documents/questions.xlsx')
        page = 1
        bot.send_message(
            message.from_user.id,
            f'<b>{df[3][page]}</b>\n\n',
            parse_mode='HTML',
            reply_markup=self._get_keyboard(page, len(df) - 1),
        )

    def _get_keyboard(self, page: int, length: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text='Ответить',
                callback_data=f'{{"method":"answer", '
                              f'"NumberPage:{page}}}',
            )
        ).add(
            InlineKeyboardButton(
                text=f'{page}/{length}',
                callback_data='  '
            ),
            InlineKeyboardButton(
                text='Вперёд --->',
                callback_data=f'{{"method":"questions", '
                              f'"NumberPage":{page + 1}, '
                              f'"CountPage"{length}}}'
            )
        )
