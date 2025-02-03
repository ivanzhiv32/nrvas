from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)

from app.presentation.handlers.base import IHandler


class TypeRecruitmentHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            'Для прохождения регистрации заполните следующую информацию:',
            reply_markup=ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text='На какой призыв Вы хотите оставить заявку?',
            reply_markup=self._get_keyboard(),
        )

    def _get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(
                'Зимний',
                callback_data='winter',
            ),
            InlineKeyboardButton(
                'Летний',
                callback_data='summer',
            )
        )
