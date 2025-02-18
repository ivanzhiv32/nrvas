from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from app.presentation.interactor import InteractorFactory


class DocumentHandler:
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc

    def __call__(self, message: Message, bot: TeleBot) -> None:
        bot.send_message(
            message.chat.id,
            text='Руковдящие документы:',
            # text='ФЗ № 53 «О воинской обязанности и военной службе» от 28.03.1998 (ред. 02.10.2024)',
            reply_markup=self._get_keyboard()
        )

    def _get_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                'ФЗ № 53 «О воинской обязанности и военной службе»',
                url='https://www.consultant.ru/document/cons_doc_LAW_18260/'
            )
        ).add(
            InlineKeyboardButton(
                'Требования к кандидатам',
                callback_data='requirements'
            )
        ).add(
            InlineKeyboardButton(
                'Перечень специальностей',
                callback_data='specialties'
            )
        )
