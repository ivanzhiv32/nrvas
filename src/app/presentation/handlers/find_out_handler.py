from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.presentation.handlers.base import IHandler
from app.presentation.handlers.sending_document_handler import (
    SendingDocumentHandler
)
from app.state import StateRecruitment


class FindOutHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'find_out',
            message.text,
            StateRecruitment.find_out
        )
        bot.send_message(
            message.chat.id,
            parse_mode='HTML',
            text='Для связи с Вами, нам необходимо получить Ваш номер телефона. '
                 'Нажмите кнопку в меню или напишите его в чат',
            reply_markup=self._get_keyboard()
        )
        self.next_handler(message, bot, SendingDocumentHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _get_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=3,
            one_time_keyboard=False
        ).add(
            KeyboardButton(
                'Отправить номер',
                request_contact=True
            )
        )
