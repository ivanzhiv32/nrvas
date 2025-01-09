from telebot import TeleBot
from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from app.state import StateRecruitment


def recruitment_callback(call: CallbackQuery, bot: TeleBot) -> None:
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.set_state(
        user_id=user_id,
        state=StateRecruitment.type_recruitment,
    )
    with bot.retrieve_data(user_id) as data:
        if call.data == 'winter':
            data['type_recruitment'] = 'Зимний'
        else:
            data['type_recruitment'] = 'Летний'

    markup = InlineKeyboardMarkup(row_width=2)

    btn_yes = InlineKeyboardButton('Да', callback_data='yes_russian')
    btn_no = InlineKeyboardButton('Нет', callback_data='no_russian')

    markup.add(btn_yes, btn_no)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text='Являетесь ли Вы гражданином Российской Федерации?',
        reply_markup=markup,
    )
