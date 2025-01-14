from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.buttons import get_nationality_keyboard
from app.presentation.interactor import InteractorFactory
from app.state import StateRecruitment


class RecruitmentCallback:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        self._set_state(call, bot)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text='Являетесь ли Вы гражданином Российской Федерации?',
            reply_markup=get_nationality_keyboard(),
        )

    def _set_state(self, call: CallbackQuery, bot: TeleBot) -> None:
        user_id = call.from_user.id
        bot.set_state(
            user_id=user_id,
            state=StateRecruitment.type_recruitment,
        )
        with bot.retrieve_data(user_id) as data:
            data['type_recruitment'] = ('Зимний' if call.data == 'winter'
                                        else 'Летний')
