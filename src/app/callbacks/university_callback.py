from telebot import TeleBot
from telebot.types import CallbackQuery

from app.constants import NO_EDUCATION
from app.handlers.candidate_data_handler import birthdate_handler


def university_callback(call: CallbackQuery, bot: TeleBot) -> None:
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if call.data == 'no_university':
        bot.send_message(chat_id=chat_id,
                         text=NO_EDUCATION)
        bot.delete_message(
            chat_id=chat_id,
            message_id=call.message.id
        )
        bot.delete_state(user_id=user_id)
        return
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.id,
        text='Напишите свою дату рождения в формате (дд.мм.гггг)'
    )
    bot.register_next_step_handler(
        call.message,
        birthdate_handler,
        bot=bot,
    )
