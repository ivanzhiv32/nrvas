from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.buttons import get_university_keyboard
from app.presentation.interactor import InteractorFactory
from app.state import StateRecruitment


class NationalityCallback:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

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
            reply_markup=get_university_keyboard(),
        )

    def _invalid_nationality(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        bot.send_message(
            chat_id=chat_id,
            text=('Извините, наличие гражданства Российской Федерации '
                  'является обязательным условием для отбора в научную роту')
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
