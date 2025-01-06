from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.constants import MILITARY_RECRUITMENT
from app.state import StateRecruitment


def type_recruitment_handler(message: Message, bot: TeleBot) -> None:
    markup = InlineKeyboardMarkup(row_width=2)

    btn_winter = InlineKeyboardButton('Зимний', callback_data='winter')
    btn_summer = InlineKeyboardButton('Летний', callback_data='summer')

    markup.add(btn_winter, btn_summer)

    bot.send_message(
        chat_id=message.chat.id,
        text=MILITARY_RECRUITMENT,
        reply_markup=markup,
    )
    bot.set_state(
        user_id=message.from_user.id,
        state=StateRecruitment.type_recruitment,
        chat_id=message.chat.id,
    )
