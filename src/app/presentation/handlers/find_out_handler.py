from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.presentation.handlers import SendingDocumentHandler
from app.presentation.handlers.base import IHandler
from app.state import StateRecruitment


class FindOutHandler(IHandler):
    def __call__(self, message: Message, bot: TeleBot) -> None:
        self.set_state(
            message,
            bot,
            'phone',
            message.text,
            StateRecruitment.find_out
        )
        bot.send_message(
            message.chat.id,
            parse_mode='HTML',
            text='Для связи с вами, нам необходимо получить ваш номер телефона. '
                 'Нажмите кнопку в меню или напишите его в чат',
            reply_markup=self._get_keyboard()
        )
        self.next_handler(message, bot, SendingDocumentHandler(self.ioc))
        bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    def _get_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
            KeyboardButton(
                'Отправить номер',
                request_contact=True
            )
        )
