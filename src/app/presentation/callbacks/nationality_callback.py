from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.presentation.buttons import get_main_keyboard
from app.presentation.callbacks.base import ICallback
from app.state import StateRecruitment


class NationalityCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        if call.data == 'no_russian':
            self._invalid_nationality(call, bot)
            return
        self._set_state(call, bot)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='Имеется ли у Вас оконченное высшее техническое образование?',
            reply_markup=self._add_keyboard(),
        )

    def _invalid_nationality(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        user_id = call.message.from_user.id
        start_command = self.ioc.start_usecase()
        bot.send_message(
            chat_id=chat_id,
            text=('Извините, наличие гражданства Российской Федерации '
                  'является обязательным условием для отбора в научную роту'),
            reply_markup=get_main_keyboard(user_id == start_command.id_admin),
        )
        bot.delete_message(
            chat_id=chat_id,
            message_id=call.message.id,
        )
        bot.delete_state(user_id=call.from_user.id)

    def _set_state(self, call: CallbackQuery, bot: TeleBot) -> None:
        user_id = call.from_user.id
        bot.set_state(
            user_id=user_id,
            state=StateRecruitment.nationality
        )
        with bot.retrieve_data(user_id) as data:
            data['nationality'] = 'Да' if call.data == 'yes_russian' else 'Нет'

    def _add_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(
                'Да',
                callback_data='yes_university'
            ),
            InlineKeyboardButton(
                'Нет',
                callback_data='no_university'
            )
        )
