from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


def documents_handler(message: Message, bot: TeleBot) -> None:
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        'Ссылка',
        url='https://www.consultant.ru/document/cons_doc_LAW_18260/',
    )
    markup.add(button1)

    bot.send_message(
        message.chat.id,
        text='ФЗ № 53 «О воинской обязанности и военной службе» от 28.03.1998 (ред. 02.10.2024)',
        reply_markup=markup
    )
