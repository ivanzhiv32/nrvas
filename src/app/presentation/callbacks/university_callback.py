from telebot import TeleBot
from telebot.types import CallbackQuery

from app.presentation.buttons import get_main_keyboard
from app.presentation.callbacks.base import ICallback
from app.presentation.handlers import BirthdateHandler
from app.presentation.interactor import InteractorFactory


class UniversityCallback(ICallback):
    def __call__(self, call: CallbackQuery, bot: TeleBot) -> None:
        if call.data == 'no_university':
            self._invalid_university(call, bot)
            return
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            text='Напишите свою дату рождения в формате (дд.мм.гггг)'
        )
        bot.register_next_step_handler(
            call.message,
            BirthdateHandler(self.ioc),
            bot=bot,
        )

    def _invalid_university(self, call: CallbackQuery, bot: TeleBot) -> None:
        chat_id = call.message.chat.id
        user_id = call.message.from_user.id
        start_command = self.ioc.start_usecase()
        bot.send_message(
            chat_id=chat_id,
            text=('Извините, наличие Высшего технического образования '
                  'является обязательным условием для отбора в научную роту'),
            reply_markup=get_main_keyboard(user_id == start_command.id_admin),
        )
        bot.delete_message(
            chat_id=chat_id,
            message_id=call.message.id
        )
        bot.delete_state(user_id=call.from_user.id)
