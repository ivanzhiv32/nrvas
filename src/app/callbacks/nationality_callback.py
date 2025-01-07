from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.constants import NO_NATIONALITY_TEXT, EDUCATION
from app.state import StateRecruitment


def nationality_callback(call: CallbackQuery, bot: TeleBot) -> None:
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    if call.data == 'no_russian':
        bot.send_message(chat_id=chat_id,
                         text=NO_NATIONALITY_TEXT)
        bot.delete_message(
            chat_id=chat_id,
            message_id=call.message.id,
        )
        bot.delete_state(user_id=user_id)
        return
    bot.set_state(
        user_id=user_id,
        state=StateRecruitment.nationality
    )

    markup = InlineKeyboardMarkup(row_width=2)

    btn_yes = InlineKeyboardButton('Да', callback_data='yes_university')
    btn_no = InlineKeyboardButton('Нет', callback_data='no_university')

    markup.add(btn_yes, btn_no)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=EDUCATION,
        reply_markup=markup,
    )
